# src/rag_api.py
import os 
from dotenv import load_dotenv
load_dotenv() # Carga el .env desde la raíz del proyecto

# --- VERIFICACIÓN INMEDIATA DE LA CLAVE ---
# Esta sección se ejecuta al inicio de Uvicorn y da feedback instantáneo.
if os.getenv("OPENROUTER_API_KEY"):
    print("✨ SUCCESS: OPENROUTER_API_KEY cargada en el entorno de inicio.")
else:
    print("⚠️ WARNING: OPENROUTER_API_KEY NO ENCONTRADA en el entorno de inicio.")
# -------------------------------------------
    
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import traceback

# vectorstore + embeddings (your installed packages)
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI(title="AI News Summarizer RAG API (robust)")

class Query(BaseModel):
    question: str
    mode: str = "summary"  # "summary" or "detailed"
    k: int = 5

# load embeddings and indexes
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load indexes (make sure these paths exist)
try:
    db_summary = FAISS.load_local("models/faiss_summaries", embeddings, allow_dangerous_deserialization=True)
    db_raw = FAISS.load_local("models/faiss_raw", embeddings, allow_dangerous_deserialization=True)
except Exception as e:
    # If load fails, set to None and return helpful error later
    db_summary = None
    db_raw = None
    print("⚠️ Warning loading FAISS indexes:", e)
    traceback.print_exc()

# Try to import RetrievalQA (may fail depending on langchain version)
USE_CHAIN = False
try:
    # prefer the "official" chain import if available
    from langchain.chains.retrieval_qa import RetrievalQA  # best attempt
    from langchain_community.llms import HuggingFaceHub
    # instantiate a simple chain factory function below if available
    USE_CHAIN = True
except Exception:
    # fallback: chain not available in this langchain install
    USE_CHAIN = False

# If chain is available, prepare an LLM (optional — may require internet/token)
LLM = None
if USE_CHAIN:
    try:
        # Using HuggingFaceHub via langchain_community if installed (may require internet)
        LLM = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature": 0.8})
    except Exception as e:
        print("⚠️ Could not initialize HuggingFaceHub LLM:", e)
        LLM = None
        USE_CHAIN = False

def docs_to_context(docs: List[Any]) -> str:
    """Join retrieved docs into a single context string (short)."""
    parts = []
    for d in docs:
        # LangChain doc object may have .page_content or .metadata
        content = getattr(d, "page_content", None) or d.metadata.get("text", None) or str(d)
        parts.append(content[:2000])  # truncate long docs
    return "\n\n---\n\n".join(parts)

@app.post("/ask")
def ask(q: Query):
    if db_summary is None or db_raw is None:
        return {"error": "FAISS indexes not found. Run build_index.py and ensure models/faiss_raw and models/faiss_summaries exist."}

    retriever = db_summary.as_retriever(search_kwargs={"k": q.k}) if q.mode == "summary" else db_raw.as_retriever(search_kwargs={"k": q.k})

    # If RetrievalQA chain is available and an LLM is ready, use it
    if USE_CHAIN and LLM is not None:
        try:
            chain = RetrievalQA.from_chain_type(llm=LLM, retriever=retriever, chain_type_kwargs={"prompt": None})
            result = chain.run(q.question)
            return {"answer": result, "sources": []}
        except Exception as e:
            print("⚠️ RetrievalQA chain failed, falling back to simple retrieval. Error:", e)

    # ---------------- Robust retriever call ----------------
    def call_retriever_get_docs(retriever, query_text):
        if hasattr(retriever, "get_relevant_documents"):
            try:
                return retriever.get_relevant_documents(query_text)
            except TypeError:
                return retriever.get_relevant_documents(query_text, run_manager=None)

        if hasattr(retriever, "_get_relevant_documents"):
            try:
                return retriever._get_relevant_documents(query_text)
            except TypeError:
                return retriever._get_relevant_documents(query_text, run_manager=None)

        if hasattr(retriever, "retrieve"):
            try:
                return retriever.retrieve(query_text)
            except TypeError:
                return retriever.retrieve(query_text, run_manager=None)

        raise RuntimeError(f"Retriever has no compatible retrieval method. Inspect retriever: {repr(retriever)}")

    docs = call_retriever_get_docs(retriever, q.question)
    context = docs_to_context(docs)

    # Build clean sources with title/url/snippet
    sources_out = []
    for d in docs:
        meta = getattr(d, "metadata", {}) or {}
        snippet = getattr(d, "page_content", "") or ""
        sources_out.append({
            "title": meta.get("title"),
            "url": meta.get("url"),
            "source": meta.get("source"),
            "pub_date": meta.get("pub_date"),
            "snippet": snippet[:450]
        })

    
    # ---------- OpenRouter synthesis (inside ask) ----------
    try:
        # Importar la clase moderna (v1.x)
        from openai import OpenAI 
    except Exception:
        OpenAI = None 

    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    answer_text = None
    if OPENROUTER_KEY and OpenAI is not None:
        
        # 1. Inicializar el cliente moderno con clave y base_url
        client = OpenAI(
            api_key=OPENROUTER_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

        # Build citation list for the prompt
        citation_lines = []
        for s in sources_out:
            title = s.get("title") or "unknown title"
            url = s.get("url") or ""
            if url:
                citation_lines.append(f"- {title}: {url}")
            else:
                citation_lines.append(f"- {title}")

        citations = "\n".join(citation_lines)

        user_prompt = (
            "You are a concise assistant. Use ONLY the provided context to answer the question. "
            "If the answer is not present in the context, say you don't know. "
            "Cite sources by title + URL.\n\n"
            f"Context:\n{context}\n\n"
            f"Sources:\n{citations}\n\n"
            f"Question: {q.question}\n\n"
            "Answer clearly and cite sources inline."
        )
        
        print("DEBUG: calling OpenRouter. key present:", bool(OPENROUTER_KEY), "model:", OPENROUTER_MODEL)

        try:
            # 2. Nueva llamada a la API usando la sintaxis moderna (client.chat.completions.create)
            resp = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": "You answer using only the provided context and cite sources."},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=350,
                temperature=0.0
            )
            # 3. Nueva forma de acceder al contenido (resp.choices[0].message.content)
            answer_text = resp.choices[0].message.content.strip() 
        except Exception as e:
            print("⚠️ OpenRouter call failed:", e)
            answer_text = None

    # If OpenRouter succeeded, return the generated answer and sources
    if answer_text:
        return {"answer": answer_text, "sources": sources_out}

    # Fallback: return retrieved context and sources if no LLM answer
    return {
        "answer": f"(retrieved {len(docs)} docs). Set OPENROUTER_API_KEY to generate a natural-language answer.",
        "context": context,
        "sources": sources_out
    }
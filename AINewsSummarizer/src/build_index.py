# src/build_index.py
import os
import pandas as pd
from datetime import date
from glob import glob

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def latest_file(path_glob):
    files = sorted(glob(path_glob))
    return files[-1] if files else None

def build_indexes():
    # embeddings and splitter (adjust chunk sizes if you want)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)

    # locate latest raw news csv
    raw_csv = latest_file("data/raw/news_*.csv")
    if not raw_csv:
        print("⚠️ No raw news CSV found in data/raw/. Run collect_news.py first.")
        return

    print("🔹 Loading raw news from:", raw_csv)
    df_raw = pd.read_csv(raw_csv).fillna("")

    raw_docs = []
    for idx, row in df_raw.iterrows():
        title = str(row.get("title", "") or "")
        description = str(row.get("description", "") or "")
        content = (title + "\n\n" + description).strip()
        url = row.get("url", "") or row.get("link", "") or ""
        source = row.get("source", "") or ""
        pub_date = row.get("publishedAt", "") or row.get("date", "")

        if not content:
            continue

        chunks = splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            meta = {"title": title, "url": url, "source": source, "pub_date": pub_date, "chunk_index": i}
            raw_docs.append(Document(page_content=chunk, metadata=meta))

    if not raw_docs:
        print("⚠️ No raw documents created — check your CSV format.")
    else:
        print(f"🔹 Built {len(raw_docs)} raw document chunks. Indexing into FAISS...")
        db_raw = FAISS.from_documents(raw_docs, embeddings)
        os.makedirs("models", exist_ok=True)
        db_raw.save_local("models/faiss_raw")
        print("✅ Raw news index saved to models/faiss_raw")

    # locate latest cluster summaries csv
    sum_csv = latest_file("data/processed/cluster_summaries_*.csv")
    if not sum_csv:
        print("⚠️ No cluster summaries CSV found in data/processed/. Run cluster_summarize.py first.")
        return

    print("🔹 Loading summaries from:", sum_csv)
    df_sum = pd.read_csv(sum_csv).fillna("")

    sum_docs = []
    for idx, row in df_sum.iterrows():
        summary = str(row.get("summary", "") or row.get("cluster_summary", "") or "")
        cluster_id = row.get("cluster_id", "") or row.get("topic", "") or idx
        meta = {"cluster_id": cluster_id}
        if not summary:
            continue
        chunks = splitter.split_text(summary)
        for i, chunk in enumerate(chunks):
            sum_docs.append(Document(page_content=chunk, metadata={**meta, "chunk_index": i}))

    if not sum_docs:
        print("⚠️ No summary documents created.")
    else:
        print(f"🔹 Built {len(sum_docs)} summary chunks. Indexing into FAISS...")
        db_sum = FAISS.from_documents(sum_docs, embeddings)
        db_sum.save_local("models/faiss_summaries")
        print("✅ Summary index saved to models/faiss_summaries")

if __name__ == "__main__":
    build_indexes()

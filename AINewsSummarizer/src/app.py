# app.py
import streamlit as st
import requests
import json

# URL de tu API RAG que está corriendo en Uvicorn (típicamente 8000)
API_URL = "http://127.0.0.1:8000/ask"

def make_api_request(question, mode, k):
    """Envía la pregunta al endpoint /ask de la API RAG."""
    payload = {
        "question": question,
        "mode": mode,
        "k": k
    }
    try:
        # Aquí se hace la llamada POST a la API
        response = requests.post(API_URL, json=payload)
        response.raise_for_status() # Lanza un error para códigos 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        # Muestra un mensaje de error si la conexión falla (por ejemplo, si la API no está corriendo)
        st.error(f"Error al conectar con la API RAG: {e}")
        st.info("Asegúrate de que la API de FastAPI esté corriendo: uvicorn src.rag_api:app --reload")
        return None

# --- Estructura de la Aplicación Streamlit ---
st.set_page_config(page_title="AI News Summarizer RAG")
st.title("📰 AI News Summarizer - Sistema RAG")
st.subheader("Pregunta sobre las noticias indexadas")

# Configuración de la barra lateral
with st.sidebar:
    st.header("⚙️ Configuración de la Búsqueda")
    
    # Selector de modo de búsqueda
    mode = st.radio(
        "Modo de Búsqueda:",
        ("summary", "detailed"),
        index=0,
        help="summary: Busca en los resúmenes de los clusters de noticias. detailed: Busca en el texto completo de las noticias."
    )
    
    # Slider para el parámetro k (número de documentos a recuperar)
    k = st.slider(
        "Número de Documentos (k):",
        min_value=1,
        max_value=15,
        value=5,
        step=1,
        help="Cuántos documentos (chunks) buscar en el índice FAISS."
    )

# Campo de entrada de la pregunta
question = st.text_input(
    "Tu Pregunta:",
    placeholder="Ej: ¿Cuáles fueron las principales noticias de tecnología de hoy?",
    key="user_question"
)

# Botón para ejecutar la consulta
if st.button("Buscar Noticias", type="primary"):
    if question:
        # 1. Ejecutar la búsqueda y esperar
        with st.spinner("Buscando y generando respuesta..."):
            api_result = make_api_request(question, mode, k)
            
        if api_result:
            st.success("Consulta Exitosa")
            
            # 2. Mostrar Respuesta del LLM
            answer_text = api_result.get('answer', 'No se pudo generar una respuesta.')
            st.markdown("### 🤖 Respuesta del Modelo")
            st.markdown(answer_text)
            
            # 3. Mostrar Fuentes
            st.markdown("### 📚 Fuentes Encontradas")
            sources = api_result.get('sources', [])
            if sources:
                for i, source in enumerate(sources):
                    title = source.get('title', 'Título Desconocido')
                    url = source.get('url', '#')
                    source_name = source.get('source', 'Fuente Desconocida')
                    snippet = source.get('snippet', 'Sin fragmento disponible')
                    pub_date = source.get('pub_date', 'Fecha Desconocida')
                    
                    st.markdown(f"**{i+1}. {title}**")
                    st.caption(f"**Fuente:** {source_name} | **Publicado:** {pub_date}")
                    st.markdown(f"🔗 [Leer Noticia Completa]({url})")
                    
                    # Mostrar el fragmento (snippet) recuperado
                    with st.expander("Fragmento Recuperado (Snippet)"):
                        st.code(snippet, language='text')
            else:
                st.info("No se encontraron fuentes relevantes.")
    else:
        st.warning("Por favor, escribe una pregunta para buscar.")
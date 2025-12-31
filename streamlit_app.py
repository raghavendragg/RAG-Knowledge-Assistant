import streamlit as st
import time
from utils.logger import AppLogger1
from config.settings import Settings
from pipeline.rag_pipeline import RAGPipeline
from app_initializer import initialize_rag_pipeline
from utils.logger import AppLogger1
import sys


# def load_rag_pipeline():
#     return initialize_rag_pipeline()


# rag_pipeline = load_rag_pipeline()

# results = rag_pipeline.run("What are the recent news about GDP?")
# print(results)

# App setup
# --------------------------------------------------
st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

logger = AppLogger1().get_logger()
logger.info("Streamlit app started")


# --------------------------------------------------
# Cache RAG pipeline (IMPORTANT)
# --------------------------------------------------
@st.cache_resource
def load_rag_pipeline():
    return initialize_rag_pipeline()

rag_pipeline = load_rag_pipeline()


# --------------------------------------------------
# UI Header
# --------------------------------------------------
st.title("📚 RAG Knowledge Assistant")
st.caption(
    "Ask questions across PDFs, Excel, CSV, and Text documents using Retrieval-Augmented Generation."
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    top_k = st.slider(
        "Number of retrieved chunks",
        min_value=1,
        max_value=10,
        value=Settings.TOP_K
    )

    show_context = st.checkbox("Show retrieved context", value=False)

    st.divider()
    st.markdown("**Tech Stack**")
    st.markdown("- Sentence Transformers")
    st.markdown("- Vector Search")
    st.markdown("- LLM")
    st.markdown("- Streamlit")

# --------------------------------------------------
# Main Query Input
# --------------------------------------------------
query = st.text_input(
    "🔎 Enter your question",
    placeholder="e.g. What does the document say about risk levels?"
)

submit = st.button("Ask")

# --------------------------------------------------
# Handle Query
# --------------------------------------------------

if submit and query.strip():
    logger.info(f"User submitted query: {query}")

    with st.spinner("Generating answer..."):
        start_time = time.time()
        try:
            st.write("### Processing your query...")
            answer = rag_pipeline.run(query)
            # st.write(f"Query: {query}")
            st.markdown("### 🧠 RAG Pipeline Response:")
            st.write(answer.content)
        except Exception as e:
            logger.exception("Error while processing query")
            st.error("Something went wrong while processing your query.")
        end_time = time.time()
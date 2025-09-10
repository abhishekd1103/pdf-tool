"""PDF Manager page for DocSuite."""
import streamlit as st
from utils.pdf_utils import PDFProcessor

def render_pdf_manager():
    tab1, tab2, tab3 = st.tabs(["🔗 PDF Merge", "❌ Page Remove", "✂️ PDF Splitter"])

    with tab1:
        render_pdf_merge()
    with tab2:
        render_page_remove()
    with tab3:
        render_pdf_splitter()

def render_pdf_merge():
    st.markdown("### 🔗 Advanced PDF Merge")
    st.info("Upload a main PDF and insert additional PDFs at specific positions")

    main_pdf = st.file_uploader("Choose the main PDF file", type=['pdf'])
    if main_pdf:
        st.success(f"✅ Main PDF: {main_pdf.name}")

def render_page_remove():
    st.markdown("### ❌ Remove Pages")
    st.info("Remove specific pages from a PDF using page ranges")

    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    if uploaded_file:
        st.success(f"✅ Loaded: {uploaded_file.name}")

def render_pdf_splitter():
    st.markdown("### ✂️ PDF Splitter")
    st.info("Split a PDF into multiple files using various methods")

    uploaded_file = st.file_uploader("Choose PDF file to split", type=['pdf'])
    if uploaded_file:
        st.success(f"✅ Loaded: {uploaded_file.name}")

#!/usr/bin/env python3
"""
DocSuite - Professional PDF Management Suite
Fully functional Streamlit application with working PDF operations
"""

import streamlit as st
import sys
from pathlib import Path

# Page configuration MUST be first
st.set_page_config(
    page_title="DocSuite - Professional PDF Management",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_css():
    """Apply modern dark theme with teal accents"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main app styling */
    .main {
        background-color: #0f1724;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1f2937;
    }

    /* Header styling */
    .docsuite-header {
        background: linear-gradient(135deg, #1f2937 0%, #0f1724 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(20, 184, 166, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .docsuite-header h1 {
        color: #14b8a6;
        margin: 0;
        font-weight: 600;
        font-size: 2.5rem;
    }

    .docsuite-header .description {
        color: #9ca3af;
        margin-top: 0.5rem;
        font-size: 1.2rem;
    }

    /* Tool cards */
    .tool-section {
        background: #1f2937;
        border: 1px solid rgba(20, 184, 166, 0.2);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #14b8a6 0%, #0f9488 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(20, 184, 166, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0f9488 0%, #0d7377 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(20, 184, 166, 0.4);
    }

    /* File uploader */
    .uploadedFile {
        border: 2px dashed #14b8a6;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: rgba(20, 184, 166, 0.05);
        margin: 1rem 0;
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        color: #10b981;
    }

    .stError {
        background-color: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        color: #ef4444;
    }

    .stWarning {
        background-color: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        color: #f59e0b;
    }

    /* Footer */
    .docsuite-footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        color: #9ca3af;
        background: #1f2937;
        border-radius: 12px;
    }

    .docsuite-footer a {
        color: #14b8a6;
        text-decoration: none;
    }

    .docsuite-footer a:hover {
        text-decoration: underline;
    }

    /* Queue display */
    .queue-item {
        background: rgba(20, 184, 166, 0.1);
        border: 1px solid rgba(20, 184, 166, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #14b8a6;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1f2937;
        border-radius: 8px 8px 0px 0px;
        color: #9ca3af;
        padding: 1rem 2rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #14b8a6;
        color: white;
    }

    /* Metrics styling */
    .metric-card {
        background: rgba(20, 184, 166, 0.1);
        border: 1px solid rgba(20, 184, 166, 0.3);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'merge_queue' not in st.session_state:
        st.session_state.merge_queue = []
    if 'main_pdf' not in st.session_state:
        st.session_state.main_pdf = None
    if 'merged_pdf' not in st.session_state:
        st.session_state.merged_pdf = None

def create_header():
    """Create professional header"""
    st.markdown("""
    <div class="docsuite-header">
        <h1>📄 DocSuite</h1>
        <div class="description">Professional PDF Management Suite</div>
    </div>
    """, unsafe_allow_html=True)

def create_footer():
    """Create footer with company info"""
    st.markdown("""
    <div class="docsuite-footer">
        <p>
            Developed by <strong>DocSuite Team</strong> | 
            Company: <a href="mailto:info@docsuite.app">DocSuite Technologies</a> | 
            Contact: <a href="mailto:support@docsuite.app">support@docsuite.app</a>
        </p>
        <p style="margin-top: 1rem; font-size: 0.9rem;">
            © 2025 DocSuite. All rights reserved. | 
            Built with ❤️ using Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Apply styling
    apply_custom_css()

    # Initialize session state
    initialize_session_state()

    # Create header
    create_header()

    # Import and render PDF manager
    from pdf_manager import render_pdf_manager
    render_pdf_manager()

    # Create footer
    create_footer()

if __name__ == "__main__":
    main()

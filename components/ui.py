"""
UI Components and styling utilities for DocSuite.
Provides reusable UI elements and custom CSS styling.
"""

import streamlit as st
from pathlib import Path

def apply_custom_css():
    """Apply custom CSS styling to the application."""

    css_content = """
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root variables */
    :root {
        --primary-color: #14b8a6;
        --background-dark: #0f1724;
        --surface-dark: #1f2937;
        --text-primary: #ffffff;
        --text-secondary: #9ca3af;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --border-radius: 8px;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Global styles */
    .main {
        padding-top: 2rem;
        font-family: 'Inter', sans-serif;
    }

    /* Header styling */
    .docsuite-header {
        background: linear-gradient(135deg, var(--surface-dark) 0%, var(--background-dark) 100%);
        padding: 2rem 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: var(--shadow);
    }

    .docsuite-header h1 {
        color: var(--primary-color);
        margin: 0;
        font-weight: 600;
        font-size: 2rem;
    }

    .docsuite-header .description {
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }

    /* Tool cards */
    .tool-card {
        background: var(--surface-dark);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .tool-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -5px rgba(20, 184, 166, 0.1);
    }

    /* Buttons */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }

    .stButton > button:hover {
        background: #0f9488;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
    }

    /* Secondary button */
    .secondary-button {
        background: transparent !important;
        border: 1px solid var(--primary-color) !important;
        color: var(--primary-color) !important;
    }

    .secondary-button:hover {
        background: var(--primary-color) !important;
        color: white !important;
    }

    /* File uploader */
    .stFileUploader {
        border: 2px dashed rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        transition: border-color 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: var(--primary-color);
    }

    /* Progress bars */
    .stProgress .st-bo {
        background-color: var(--primary-color);
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid var(--success-color);
    }

    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid var(--error-color);
    }

    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid var(--warning-color);
    }

    /* Sidebar customization */
    .css-1d391kg {
        background-color: var(--background-dark);
    }

    .css-1y4p8pa {
        background-color: var(--surface-dark);
        border-radius: var(--border-radius);
        margin-bottom: 1rem;
    }

    /* Footer */
    .docsuite-footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        color: var(--text-secondary);
    }

    .docsuite-footer a {
        color: var(--primary-color);
        text-decoration: none;
    }

    .docsuite-footer a:hover {
        text-decoration: underline;
    }

    /* Queue display */
    .merge-queue-item {
        background: var(--surface-dark);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid var(--primary-color);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .docsuite-header {
            padding: 1rem;
        }

        .docsuite-header h1 {
            font-size: 1.5rem;
        }

        .tool-card {
            padding: 1rem;
        }
    }
    </style>
    """

    st.markdown(css_content, unsafe_allow_html=True)

def create_header(tool_info):
    """Create the application header with tool information."""
    if tool_info:
        st.markdown(f"""
        <div class="docsuite-header">
            <h1>{tool_info['icon']} {tool_info['name']}</h1>
            <div class="description">{tool_info['description']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="docsuite-header">
            <h1>📄 DocSuite</h1>
            <div class="description">Professional PDF Management Suite</div>
        </div>
        """, unsafe_allow_html=True)

def create_footer():
    """Create the application footer with developer and company information."""
    st.markdown("""
    <div class="docsuite-footer">
        <p>
            Developed by <strong>DocSuite Team</strong> | 
            Company: <a href="mailto:info@docsuite.app">DocSuite Technologies</a> | 
            Contact: <a href="mailto:support@docsuite.app">support@docsuite.app</a> | 
            © 2025 DocSuite. All rights reserved.
        </p>
        <p style="margin-top: 1rem; font-size: 0.9rem;">
            Built with ❤️ using Streamlit | 
            <a href="https://github.com/docsuite/docsuite">GitHub</a> | 
            <a href="#privacy">Privacy Policy</a> | 
            <a href="#terms">Terms of Service</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_tool_card(title, description, icon="🔧"):
    """Create a styled tool card component."""
    st.markdown(f"""
    <div class="tool-card">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def show_success_message(message):
    """Display a styled success message."""
    st.success(f"✅ {message}")

def show_error_message(message):
    """Display a styled error message."""
    st.error(f"❌ {message}")

def show_warning_message(message):
    """Display a styled warning message."""
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    """Display a styled info message."""
    st.info(f"ℹ️ {message}")

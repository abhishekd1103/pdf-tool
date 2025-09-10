#!/usr/bin/env python3
"""
DocSuite - Professional PDF Management Suite
Main application entry point with modular architecture and plugin system.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from components.ui import apply_custom_css, create_header, create_footer
from components.sidebar import create_sidebar
from tools.registry import discover_tools, get_tool_by_name

# Page configuration
st.set_page_config(
    page_title="DocSuite - Professional PDF Management",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'current_tool' not in st.session_state:
        st.session_state.current_tool = 'PDF Manager'

    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}

    if 'merge_queue' not in st.session_state:
        st.session_state.merge_queue = []

    if 'merged_pdf' not in st.session_state:
        st.session_state.merged_pdf = None

def main():
    """Main application function."""

    # Apply custom styling
    apply_custom_css()

    # Initialize session state
    initialize_session_state()

    # Discover available tools
    available_tools = discover_tools()

    # Create sidebar navigation
    selected_tool = create_sidebar(available_tools, st.session_state.current_tool)

    # Update current tool if changed
    if selected_tool != st.session_state.current_tool:
        st.session_state.current_tool = selected_tool
        st.rerun()

    # Create header
    tool_info = get_tool_by_name(selected_tool, available_tools)
    create_header(tool_info)

    # Render the selected tool
    if tool_info:
        try:
            tool_info['render_function']()
        except Exception as e:
            st.error(f"Error loading tool '{selected_tool}': {str(e)}")
            st.write("Please check the tool implementation or contact support.")
    else:
        st.error(f"Tool '{selected_tool}' not found!")

    # Create footer
    create_footer()

if __name__ == "__main__":
    main()

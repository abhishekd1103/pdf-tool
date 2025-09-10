"""Sidebar navigation component for DocSuite."""
import streamlit as st

def create_sidebar(available_tools, current_tool):
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #14b8a6; margin: 0;">📄 DocSuite</h1>
            <p style="color: #9ca3af; margin: 0.5rem 0;">Professional PDF Tools</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔧 Available Tools")

        selected_tool = None
        for tool in available_tools:
            tool_name = tool['name']
            is_current = tool_name == current_tool

            if st.button(
                f"{tool['icon']} {tool_name}",
                key=f"tool_{tool_name}",
                help=tool['description'],
                use_container_width=True,
                type="primary" if is_current else "secondary"
            ):
                selected_tool = tool_name

        if selected_tool is None:
            selected_tool = current_tool

        return selected_tool

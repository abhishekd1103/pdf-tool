"""Plot Digitizer Tool Template."""
import streamlit as st

def get_tool_info():
    return {
        "name": "Plot Digitizer",
        "description": "Extract data points from plots and graphs (Coming Soon)",
        "icon": "📊"
    }

def render_tool():
    st.info("🚧 **Plot Digitizer - Coming Soon!**")
    st.markdown("This tool will allow you to extract data from plots and charts.")

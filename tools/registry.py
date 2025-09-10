"""Tool registry and auto-discovery system."""
import streamlit as st

def discover_tools():
    tools = []
    tools.append({
        'name': 'PDF Manager',
        'description': 'Advanced PDF manipulation tools: merge, split, remove pages',
        'icon': '📄',
        'render_function': _render_pdf_manager
    })
    return tools

def get_tool_by_name(tool_name, available_tools):
    for tool in available_tools:
        if tool['name'] == tool_name:
            return tool
    return None

def _render_pdf_manager():
    from pages.pdf_manager import render_pdf_manager
    render_pdf_manager()

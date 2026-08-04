import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, premium_card

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")
inject_global_css()
section_title("About AI Career Intelligence", "ℹ️")
premium_card("Our Mission", "To empower tech professionals by providing AI-driven insights into their resumes and career paths.", "🚀")

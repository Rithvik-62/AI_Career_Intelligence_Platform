import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
inject_global_css()

try:
    section_title("Settings", "⚙️")
    st.markdown("Application settings and configurations.")
    
    st.markdown("---")
    st.markdown("### Session Management")
    
    if st.button("🔄 Reset Current Session", type="primary"):
        st.session_state.clear()
        st.success("Session cleared successfully! Please return to the Home page.")
        
    st.markdown("---")
    st.markdown("### System Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Version:** 1.0.0 (Production)")
        st.markdown("**Environment:** Windows / Streamlit Engine")
        st.markdown("**ML Backend:** Scikit-Learn Decision Trees")
    with col2:
        st.markdown("**NLP Backend:** pdfplumber, NLTK")
        st.markdown("**UI Framework:** Streamlit, Plotly")
        st.markdown("**Status:** System Healthy ✅")
        
except Exception as e:
    import traceback
    st.error("An unexpected error occurred while loading this page.")
    with st.expander("Details"): st.code(traceback.format_exc())

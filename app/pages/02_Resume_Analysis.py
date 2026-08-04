import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, render_experience_card, render_project_card, render_education_card, premium_card

st.set_page_config(page_title="Resume Analysis", page_icon="📄", layout="wide")
inject_global_css()

try:
    section_title("Resume Analysis", "📄")
    if 'parsed_data' not in st.session_state or st.session_state['parsed_data'] is None:
        st.warning("Please upload a resume on the Home page first.")
    else:
        data = st.session_state['parsed_data']
        
        # Display Basic Info
        st.markdown("### Contact Information")
        contact_html = f"""
        <div style="display:flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px;">
            <div><strong>Email:</strong> {data.get('email', 'N/A')}</div>
            <div><strong>Phone:</strong> {data.get('phone', 'N/A')}</div>
            <div><strong>Location:</strong> {data.get('location', 'N/A')}</div>
        </div>
        """
        st.markdown(contact_html, unsafe_allow_html=True)
        
        # Display Skills
        st.markdown("### Technical Skills")
        skills = data.get("skills", [])
        if skills:
            skills_html = "<div style='display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;'>"
            for skill in skills:
                skills_html += f"<span style='background:rgba(37,99,235,0.15); color:var(--primary); padding:4px 12px; border-radius:12px; border:1px solid rgba(37,99,235,0.3);'>{skill}</span>"
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No skills explicitly detected.")
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Experience")
            exp = data.get("experience", [])
            if not exp:
                st.info("No work experience found.")
            for e in exp:
                render_experience_card(e)
                
            st.markdown("### Education")
            edu = data.get("education", [])
            if not edu:
                st.info("No education records found.")
            for e in edu:
                render_education_card(e)
                
        with col2:
            st.markdown("### Projects")
            proj = data.get("projects", [])
            if not proj:
                st.info("No projects found.")
            for p in proj:
                render_project_card(p)
                
except Exception as e:
    import traceback
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from utils.logger import app_logger
    app_logger.error(f'Error in {os.path.basename(__file__)}: {str(e)}\n{traceback.format_exc()}')
    st.error('An unexpected error occurred while loading this page.')
    with st.expander('View Technical Details'):
        st.code(traceback.format_exc())

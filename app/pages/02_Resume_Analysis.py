import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, render_experience_card, render_project_card, render_education_card, premium_card, render_aria_sidebar_chatbot, status_chip

st.set_page_config(page_title="Resume Deep Extraction", page_icon="📄", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

def format_url_link(url_val, default_label):
    if isinstance(url_val, str) and url_val.startswith("http"):
        return f'<a href="{url_val}" target="_blank" style="color:var(--accent);">{url_val}</a>'
    elif isinstance(url_val, str) and url_val.strip():
        return url_val.strip()
    return default_label

try:
    section_title("Resume Deep Extraction & Parsing Engine", "📄")
    if 'parsed_data' not in st.session_state or st.session_state['parsed_data'] is None:
        st.warning("Please upload a resume on the Home page first to view extracted structured data.")
    else:
        data = st.session_state['parsed_data']
        
        name = data.get('name') or 'Name Not Detected'
        email = data.get('email') or 'Email Not Found'
        phone = data.get('phone') or 'Phone Not Found'
        location = data.get('location') or 'Location Not Specified'
        linkedin_val = data.get('linkedin')
        github_val = data.get('github')
        portfolio_val = data.get('portfolio')
        
        linkedin_display = format_url_link(linkedin_val, "LinkedIn Not Provided")
        github_display = format_url_link(github_val, "GitHub Not Provided")
        portfolio_display = format_url_link(portfolio_val, "Portfolio Not Provided")
        
        confidence = data.get('metadata', {}).get('parsing_confidence', 0.0) if isinstance(data.get('metadata'), dict) else 0.0

        # 1. Candidate Hero Header Card
        st.markdown(
            f'<div class="premium-card" style="border-left: 4px solid var(--accent); margin-bottom:24px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">'
            f'<div>'
            f'<div style="font-size:0.82rem; color:var(--accent); font-weight:700; letter-spacing:1px; text-transform:uppercase;">Extracted Candidate Profile</div>'
            f'<h2 style="margin:4px 0 8px 0; font-size:2rem; font-weight:800;">{name}</h2>'
            f'<div style="color:var(--text-muted); font-size:0.92rem; display:flex; gap:18px; flex-wrap:wrap;">'
            f'<span>📧 {email}</span>'
            f'<span>📞 {phone}</span>'
            f'<span>📍 {location}</span>'
            f'</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:4px;">Parsing Confidence Index</div>'
            f'<div style="font-size:2rem; font-weight:800; color:var(--success); font-family:\'Outfit\', sans-serif;">{confidence:.1f}%</div>'
            f'</div>'
            f'</div>'
            f'<div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08); display:flex; gap:16px; flex-wrap:wrap; font-size:0.88rem;">'
            f'<span>🔗 <strong>LinkedIn:</strong> {linkedin_display}</span>'
            f'<span>💻 <strong>GitHub:</strong> {github_display}</span>'
            f'<span>🌐 <strong>Portfolio:</strong> {portfolio_display}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # 2. Display Technical Skills
        st.markdown("### ⚡ Extracted Technical Skills")
        skills = data.get("skills", [])
        if skills:
            chips = "".join([status_chip(skill, "primary") for skill in skills])
            st.markdown(f"<div style='margin-bottom:24px;'>{chips}</div>", unsafe_allow_html=True)
        else:
            st.info("No technical skills explicitly detected in document text.")

        st.markdown("---")

        # 3. Section Cards Breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🏢 Work Experience")
            exp = data.get("experience", [])
            if not exp:
                st.info("No work experience records found.")
            for e in exp:
                if isinstance(e, dict):
                    render_experience_card(e)

            st.markdown("### 🏛️ Education Records")
            edu = data.get("education", [])
            if not edu:
                st.info("No education records found.")
            for e in edu:
                if isinstance(e, dict):
                    render_education_card(e)

        with col2:
            st.markdown("### 💻 Projects & Systems")
            proj = data.get("projects", [])
            if not proj:
                st.info("No projects found.")
            for p in proj:
                if isinstance(p, dict):
                    render_project_card(p)

            st.markdown("### 📜 Certifications & Achievements")
            certs = data.get("certifications", [])
            achievements = data.get("achievements", [])
            if not certs and not achievements:
                st.info("No certifications or achievements specified.")
            for c in certs:
                st.markdown(f"<div class='premium-card' style='padding:14px; margin-bottom:10px;'>📜 <strong>{c}</strong></div>", unsafe_allow_html=True)
            for a in achievements:
                st.markdown(f"<div class='premium-card' style='padding:14px; margin-bottom:10px;'>🏆 <strong>{a}</strong></div>", unsafe_allow_html=True)

except Exception as e:
    import traceback
    st.error('An unexpected error occurred while loading Resume Analysis.')
    with st.expander('View Technical Details'):
        st.code(traceback.format_exc())

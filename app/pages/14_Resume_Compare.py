import streamlit as st
import sys, os, tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, status_chip, apply_plotly_theme, render_aria_sidebar_chatbot
from utils.parser import ResumeParser
from utils.scoring import ResumeScorer
from utils.resume_comparator import ResumeComparator
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Candidate Comparison Mode", page_icon="🆚", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Candidate Resume Comparison Mode", "🆚")
    st.markdown("Compare your active resume against another candidate's uploaded PDF resume side-by-side.")
    
    # Candidate A (Active Session Data or Fallback)
    candA = {
        'name': 'Candidate A (Your Resume)',
        'skills': ['Python', 'SQL', 'Machine Learning', 'TensorFlow', 'Pandas', 'Scikit-Learn'],
        'projects': [{'project_title': 'P1'}, {'project_title': 'P2'}],
        'experience': [{'job_title': 'E1'}]
    }
    scoreA = {'overall_score': 88, 'ats_score': 90, 'completeness_pct': 92}
    
    if 'parsed_data' in st.session_state and st.session_state['parsed_data'] is not None:
        candA['name'] = st.session_state['parsed_data'].get('name', 'Your Active Resume')
        candA['skills'] = st.session_state['parsed_data'].get('skills', [])
        candA['projects'] = st.session_state['parsed_data'].get('projects', [])
        candA['experience'] = st.session_state['parsed_data'].get('experience', [])
        scoreA = st.session_state.get('scoring_data', scoreA)

    # Candidate B Uploader Zone
    st.markdown("### 📄 Upload Candidate B's Resume (PDF)")
    col_up, col_info = st.columns([2, 1])
    
    candB = {
        'name': 'Candidate B (Competitor Profile)',
        'skills': ['Java', 'Spring Boot', 'SQL', 'Docker', 'Git', 'Kubernetes'],
        'projects': [{'project_title': 'P1'}],
        'experience': [{'job_title': 'E1'}, {'job_title': 'E2'}]
    }
    scoreB = {'overall_score': 82, 'ats_score': 85, 'completeness_pct': 88}

    with col_up:
        uploaded_B = st.file_uploader("Upload Candidate B PDF Resume", type="pdf")
        if uploaded_B is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(uploaded_B.getvalue())
                tmp_path = tmp.name
                
            parser = ResumeParser()
            parsedB = parser.parse(tmp_path)
            if "error" not in parsedB:
                scorer = ResumeScorer()
                scoreB = scorer.score_resume(parsedB)
                candB['name'] = parsedB.get('name', uploaded_B.name.replace('.pdf', ''))
                candB['skills'] = parsedB.get('skills', [])
                candB['projects'] = parsedB.get('projects', [])
                candB['experience'] = parsedB.get('experience', [])
                st.success(f"✅ Successfully parsed {candB['name']}!")
            os.remove(tmp_path)

    st.markdown("---")

    # Perform Side-by-Side Comparison
    res = ResumeComparator.compare_candidates(candA, scoreA, candB, scoreB)
    
    col1, col2 = st.columns(2)
    with col1:
        metric_card(res['nameA'], f"{scoreA.get('overall_score', 0)}/100", "👤", "Candidate A Score")
    with col2:
        metric_card(res['nameB'], f"{scoreB.get('overall_score', 0)}/100", "👤", "Candidate B Score")

    st.markdown("---")

    # Metrics DataFrame Table
    st.markdown("### 📊 Metric Comparison Matrix")
    st.dataframe(res['comparison_df'], use_container_width=True, hide_index=True)

    st.markdown("---")

    # Radar Comparison Chart
    st.markdown("### 🕸️ Overlay Category Radar Comparison")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[scoreA.get('overall_score',0), scoreA.get('ats_score',0), scoreA.get('completeness_pct',0)], 
        theta=['Overall Score', 'ATS Score', 'Completeness %'], fill='toself', name=res['nameA']
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[scoreB.get('overall_score',0), scoreB.get('ats_score',0), scoreB.get('completeness_pct',0)], 
        theta=['Overall Score', 'ATS Score', 'Completeness %'], fill='toself', name=res['nameB']
    ))
    apply_plotly_theme(fig_radar)
    fig_radar.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100])))
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🤝 Common Skills")
        st.markdown("".join([status_chip(s, "primary") for s in res['common_skills']]), unsafe_allow_html=True)
    with c2:
        st.markdown(f"#### ⚡ Unique to {res['nameA']}")
        st.markdown("".join([status_chip(s, "success") for s in res['uniqueA']]), unsafe_allow_html=True)
    with c3:
        st.markdown(f"#### ⚡ Unique to {res['nameB']}")
        st.markdown("".join([status_chip(s, "accent") for s in res['uniqueB']]), unsafe_allow_html=True)

except Exception as e:
    import traceback
    st.error("An unexpected error occurred during Candidate Comparison.")
    with st.expander("Details"): st.code(traceback.format_exc())

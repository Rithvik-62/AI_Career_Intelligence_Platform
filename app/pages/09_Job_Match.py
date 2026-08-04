import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, status_chip, apply_plotly_theme, render_aria_sidebar_chatbot
from utils.matcher import JobDescriptionMatcher
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Resume vs JD Match Engine", page_icon="🎯", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Resume vs Job Description Match Engine", "🎯")
    
    if 'parsed_data' not in st.session_state or st.session_state['parsed_data'] is None:
        st.warning("Please upload a resume or select a Demo Profile on the Home page first.")
    else:
        parsed_data = st.session_state['parsed_data']
        resume_skills = parsed_data.get('skills', [])
        
        # Build text string from parsed resume elements
        resume_text_repr = f"Skills: {', '.join(resume_skills)}. "
        for exp in parsed_data.get('experience', []):
            if isinstance(exp, dict):
                resume_text_repr += f"{exp.get('job_title', '')} {exp.get('company', '')} {exp.get('description', '')}. "
        for proj in parsed_data.get('projects', []):
            if isinstance(proj, dict):
                resume_text_repr += f"{proj.get('project_title', '')} {proj.get('description', '')}. "
                
        st.markdown("### 📝 Target Job Description")
        jd_input = st.text_area(
            "Paste Job Description text below to evaluate TF-IDF Cosine Similarity and Skill Intersection:",
            height=180,
            placeholder="e.g. Seeking a Senior Data Scientist proficient in Python, SQL, PyTorch, Docker, and AWS..."
        )
        
        if st.button("⚡ Run Job Description Match Analysis", type="primary", use_container_width=True):
            if not jd_input.strip():
                st.error("Please paste a target Job Description text.")
            else:
                matcher = JobDescriptionMatcher()
                match_res = matcher.match(resume_text_repr, jd_input)
                st.session_state['match_data'] = match_res
                
        # Display Results if present
        if 'match_data' in st.session_state and st.session_state['match_data'] is not None:
            res = st.session_state['match_data']
            if "error" not in res:
                st.markdown("---")
                
                # 1. Metrics Row
                m1, m2, m3 = st.columns(3)
                with m1: metric_card("Cosine Similarity Match", f"{res['match_score']}%", "📐", "TF-IDF Vector Space Fit")
                with m2: metric_card("JD Skill Coverage", f"{res['skill_coverage']}%", "🎯", "Target Skill Coverage")
                with m3: metric_card("Employability Index", f"{res['employability_score']}%", "🏆", "Composite Match Index")

                st.markdown("---")

                # 2. Charts
                col_chart1, col_chart2 = st.columns(2)
                with col_chart1:
                    st.markdown("#### 🎛️ Cosine Similarity Match Gauge")
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number", value=res['match_score'],
                        title={'text': "Semantic Match %"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#7C3AED"},
                            'steps': [{'range': [0, 50], 'color': "rgba(239,68,68,0.3)"}, {'range': [50, 75], 'color': "rgba(245,158,11,0.3)"}, {'range': [75, 100], 'color': "rgba(16,185,129,0.3)"}]
                        }
                    ))
                    apply_plotly_theme(fig_gauge)
                    fig_gauge.update_layout(height=260)
                    st.plotly_chart(fig_gauge, use_container_width=True)

                with col_chart2:
                    st.markdown("#### 🍩 Skill Intersection Donut")
                    cnt_match = len(res.get('matched_skills', []))
                    cnt_miss = len(res.get('missing_skills', []))
                    
                    if cnt_match == 0 and cnt_miss == 0:
                        # Fallback if no explicit skills detected in JD text
                        st.info("💡 Paste a detailed Job Description with technical skills (e.g. Python, SQL, AWS) to render the skill intersection donut.")
                    else:
                        df_d = pd.DataFrame({'Status': ['Matched', 'Missing'], 'Count': [cnt_match, cnt_miss]})
                        fig_d = px.pie(df_d, values='Count', names='Status', hole=0.55, color='Status', color_discrete_map={'Matched':'#10B981', 'Missing':'#EF4444'})
                        apply_plotly_theme(fig_d)
                        fig_d.update_layout(height=260)
                        st.plotly_chart(fig_d, use_container_width=True)

                st.markdown("---")

                # 3. Matched vs Missing Skills breakdown
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### ✅ Matched JD Skills")
                    if res['matched_skills']:
                        st.markdown("".join([status_chip(s, "success") for s in res['matched_skills']]), unsafe_allow_html=True)
                    else:
                        st.caption("No overlapping skills detected.")
                with c2:
                    st.markdown("#### ⚠️ Missing Critical JD Skills")
                    if res['missing_skills']:
                        st.markdown("".join([status_chip(s, "danger") for s in res['missing_skills']]), unsafe_allow_html=True)
                    else:
                        st.success("All required skills present!")

                st.markdown("---")
                st.markdown("#### 💡 Prescriptive Match Recommendations")
                for rec in res.get('recommendations', []):
                    st.markdown(
                        f'<div class="premium-card" style="padding:15px; border-left:3px solid var(--accent); margin-bottom:8px;">'
                        f'⚡ {rec}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while executing Job Description Match Engine.")
    with st.expander("Details"): st.code(traceback.format_exc())

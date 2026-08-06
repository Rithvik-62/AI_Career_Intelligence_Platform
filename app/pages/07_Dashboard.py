import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, apply_plotly_theme, render_aria_sidebar_chatbot
from utils.gemini_service import GeminiService
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Executive BI Dashboard", page_icon="📈", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Power BI Executive Analytics Dashboard", "📈")
    
    if 'parsed_data' not in st.session_state or st.session_state['parsed_data'] is None:
        st.info("Upload a resume or select a Demo Profile on the Home page to populate the executive dashboard.")
    else:
        parsed_data = st.session_state.get('parsed_data', {})
        prediction_data = st.session_state.get('prediction_data', {})
        scoring_data = st.session_state.get('scoring_data', {})
        skill_gap_data = st.session_state.get('skill_gap_data', {})
        insights_data = st.session_state.get('insights_data', {})

        score = scoring_data.get('overall_score', 0)
        ats = scoring_data.get('ats_score', 0)
        role = prediction_data.get('predicted_role', 'Unknown')
        conf = prediction_data.get('confidence', 0.0)
        readiness = scoring_data.get('career_readiness', 0.0)
        completeness = scoring_data.get('completeness_pct', 0.0)

        # 1. Gemini AI Executive Summary Card
        st.markdown(
            f'<div class="premium-card" style="border-left:4px solid var(--primary); background:linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(6,182,212,0.08) 100%);">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">'
            f'<h3 style="margin:0; color:var(--accent);">🤖 Gemini AI Executive Summary</h3>'
            f'<span style="font-size:0.78rem; background:rgba(6,182,212,0.15); color:var(--accent); padding:3px 10px; border-radius:12px; border:1px solid rgba(6,182,212,0.3);">Real-Time Intelligence</span>'
            f'</div>'
            f'<p style="color:var(--text-muted); font-size:0.98rem; line-height:1.6; margin:0;">'
            f'Candidate <strong>{parsed_data.get("name", "Alex Rivera")}</strong> exhibits an overall profile score of <strong>{score}/100</strong> '
            f'with an ATS compatibility index of <strong>{ats}%</strong>. Primary machine learning classification identifies a strong statistical trajectory towards '
            f'<strong>{role}</strong> ({conf}% confidence). Key missing competencies to unlock top-tier roles: <strong>{", ".join(skill_gap_data.get("missing_skills", [])[:3])}</strong>.'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # 2. Executive KPI Cards Row (6 Cards)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: metric_card("Resume Score", f"{score}/100", "🏆", "Composite Quality")
        with c2: metric_card("ATS Compatibility", f"{ats}%", "🤖", "Readability Index")
        with c3: metric_card("Career Readiness", f"{readiness}%", "🎯", "Target Job Fit")
        with c4: metric_card("Predicted Role", role, "🔮", f"{conf}% Conf.")
        with c5: metric_card("Completeness", f"{completeness}%", "📋", "Section Coverage")
        with c6: metric_card("Skill Coverage", f"{skill_gap_data.get('coverage_pct', 0)}%", "⚡", "Required Skills")

        st.markdown("---")
        
        # 3. Descriptive & Predictive Visualizations
        st.markdown("### 📊 Descriptive & Predictive Analytics Visualizations")
        r1_c1, r1_c2, r1_c3 = st.columns(3)
        
        with r1_c1:
            st.markdown("#### 🕸️ Structural Density Radar")
            cat_scores = scoring_data.get('category_scores', {})
            df_radar = pd.DataFrame(dict(
                r=[cat_scores.get('skills',0)/30*100, cat_scores.get('experience',0)/20*100, 
                   cat_scores.get('projects',0)/20*100, cat_scores.get('education',0)/15*100, 
                   cat_scores.get('certifications',0)/15*100],
                theta=['Skills', 'Experience', 'Projects', 'Education', 'Certs']))
            fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
            fig_radar.update_traces(fill='toself', line_color='#2563EB', fillcolor="rgba(37,99,235,0.25)")
            apply_plotly_theme(fig_radar)
            fig_radar.update_layout(height=260, polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100])))
            st.plotly_chart(fig_radar, use_container_width=True)
            st.caption("🔍 **Insight:** Structural density across key resume categories.")

        with r1_c2:
            st.markdown("#### 🎛️ AI Prediction Confidence Gauge")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=conf,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#06B6D4"},
                    'steps': [
                        {'range': [0, 60], 'color': "rgba(239, 68, 68, 0.2)"},
                        {'range': [60, 85], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [85, 100], 'color': "rgba(34, 197, 94, 0.2)"}
                    ]
                }
            ))
            apply_plotly_theme(fig_gauge)
            fig_gauge.update_layout(height=260)
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.caption(f"🔮 **Insight:** ML Leaf probability for **{role}**.")

        with r1_c3:
            st.markdown("#### 🍩 Skill Match Ratio Donut")
            acquired_cnt = len(skill_gap_data.get('acquired_skills', []))
            missing_cnt = len(skill_gap_data.get('missing_skills', []))
            df_donut = pd.DataFrame({'Status': ['Acquired', 'Missing'], 'Count': [acquired_cnt, missing_cnt]})
            fig_donut = px.pie(df_donut, values='Count', names='Status', hole=0.55, color='Status', color_discrete_map={'Acquired':'#22C55E', 'Missing':'#EF4444'})
            apply_plotly_theme(fig_donut)
            fig_donut.update_layout(height=260)
            st.plotly_chart(fig_donut, use_container_width=True)
            st.caption(f"⚡ **Insight:** {acquired_cnt} acquired, {missing_cnt} missing skills.")

        st.markdown("---")
        
        # 4. Advanced BI Visualizations
        st.markdown("### 🧩 Advanced Business Intelligence Visualizations")
        r2_c1, r2_c2 = st.columns(2)
        
        with r2_c1:
            st.markdown("#### 🗺️ Skill Category Treemap")
            skills_list = parsed_data.get('skills', ['Python', 'SQL'])
            df_tree = pd.DataFrame({
                'Category': ['Technical Skills'] * len(skills_list),
                'Skill': [s.title() for s in skills_list],
                'Value': [1] * len(skills_list)
            })
            fig_tree = px.treemap(df_tree, path=['Category', 'Skill'], values='Value', color='Value', color_continuous_scale='Blues')
            apply_plotly_theme(fig_tree)
            fig_tree.update_layout(height=280)
            st.plotly_chart(fig_tree, use_container_width=True)
            st.caption("📌 **Insight:** Hierarchy of extracted technical keywords.")

        with r2_c2:
            st.markdown("#### ☀️ Category Performance Heatmap")
            df_heat = pd.DataFrame({
                'Metric': ['Skills Score', 'Experience Score', 'Projects Score', 'Education Score', 'Certifications Score'],
                'Performance %': [
                    cat_scores.get('skills',0)/30*100,
                    cat_scores.get('experience',0)/20*100,
                    cat_scores.get('projects',0)/20*100,
                    cat_scores.get('education',0)/15*100,
                    cat_scores.get('certifications',0)/15*100
                ]
            })
            fig_heat = px.density_heatmap(df_heat, x='Metric', y='Performance %', z='Performance %', color_continuous_scale='Blues')
            apply_plotly_theme(fig_heat)
            fig_heat.update_layout(height=280)
            st.plotly_chart(fig_heat, use_container_width=True)
            st.caption("🔥 **Insight:** Heatmap highlighting section strengths vs bottlenecks.")

        st.markdown("---")
        
        # 5. Actions & Executive PDF Report Export
        st.markdown("### 📥 Executive Actions & Reporting")
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            try:
                from utils.pdf_generator import generate_pdf_report
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    generate_pdf_report(st.session_state, tmp.name)
                    with open(tmp.name, "rb") as pdf_file: 
                        pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📥 Export Executive PDF Report", 
                    data=pdf_bytes, 
                    file_name="Executive_Career_Analytics_Report.pdf", 
                    mime="application/pdf", 
                    use_container_width=True
                )
            except Exception as pdf_err:
                st.error(f"PDF Export Error: {str(pdf_err)}")
                
        with btn_c2:
            if st.button("🔄 Reset Session State", use_container_width=True):
                st.session_state.clear()
                st.switch_page("pages/01_Home.py")

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while rendering the Executive BI Dashboard.")
    with st.expander("Details"): st.code(traceback.format_exc())

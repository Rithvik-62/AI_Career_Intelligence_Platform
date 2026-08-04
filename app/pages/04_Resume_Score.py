import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, apply_plotly_theme, render_aria_sidebar_chatbot
from utils.rewriter import ResumeRewriter
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Advanced Resume Analytics", page_icon="📊", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Advanced Resume Analytics", "📊")
    
    if 'scoring_data' not in st.session_state or st.session_state['scoring_data'] is None:
        st.warning("Please upload a resume on the Home page first to compute analytics.")
    else:
        data = st.session_state['scoring_data']
        parsed_data = st.session_state.get('parsed_data', {})
        prediction_data = st.session_state.get('prediction_data', {})
        
        overall = data.get('overall_score', 0)
        ats = data.get('ats_score', 0)
        completeness = data.get('completeness_pct', 0.0)
        readiness = data.get('career_readiness', 0.0)
        rating = data.get('rating', 'Unknown')
        categories = data.get('category_scores', {})
        interpretations = data.get('interpretations', {})
        
        # 1. KPI Metric Row
        k1, k2, k3, k4 = st.columns(4)
        with k1: metric_card("Overall Resume Score", f"{overall}/100", "🏆", rating)
        with k2: metric_card("ATS Compatibility", f"{ats}%", "🤖", "Structural Readability")
        with k3: metric_card("Resume Completeness", f"{completeness}%", "📋", "Core Section Presence")
        with k4: metric_card("Career Readiness", f"{readiness}%", "🎯", "Employability Index")

        st.markdown("---")

        # 2. Detailed Scores Breakdown & Visualizations
        col_main, col_chart = st.columns([1, 1.2])
        
        with col_main:
            st.markdown("### 📈 Granular Category Scores & Interpretations")
            max_scores = {'skills': 30, 'education': 15, 'projects': 20, 'experience': 20, 'certifications': 15}
            
            for cat, score in categories.items():
                max_val = max_scores.get(cat, 100)
                pct = int((score / max_val) * 100)
                color = "#22c55e" if pct >= 75 else "#f59e0b" if pct >= 50 else "#ef4444"
                
                st.markdown(f"**{cat.title()} Score:** {score} / {max_val} ({pct}%)")
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.08); border-radius:6px; height:10px; margin-bottom:6px;">
                    <div style="background:{color}; width:{pct}%; height:100%; border-radius:6px;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                interp = interpretations.get(cat, f"{cat.title()} evaluated at {score}/{max_val}.")
                st.caption(f"💡 *{interp}*")
                st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

        with col_chart:
            st.markdown("### 🕸️ Structural Density Radar Matrix")
            df_radar = pd.DataFrame(dict(
                r=[categories.get('skills',0)/max_scores['skills']*100, 
                   categories.get('experience',0)/max_scores['experience']*100, 
                   categories.get('projects',0)/max_scores['projects']*100, 
                   categories.get('education',0)/max_scores['education']*100, 
                   categories.get('certifications',0)/max_scores['certifications']*100],
                theta=['Skills', 'Experience', 'Projects', 'Education', 'Certifications']))
            
            fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True, title="Category Score % Density")
            fig_radar.update_traces(fill='toself', line_color='#2563eb', fillcolor="rgba(37,99,235,0.2)")
            fig_radar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0, 100])),
                font=dict(color="#F8FAFC"), margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("---")
        
        # 3. Resume Rewriter Suggestion Engine Panel
        st.markdown("### ✍️ AI Resume Rewriter (Before vs After Action Bullets)")
        st.caption("Quantifiable, impact-driven bullet point recommendations for your target career.")
        
        target_r = prediction_data.get('predicted_role', 'Software Developer')
        rewrites = ResumeRewriter.get_rewriter_suggestions(parsed_data, target_r)
        
        for rw in rewrites:
            st.markdown(f"""
            <div class="premium-card" style="border-left: 4px solid var(--accent); margin-bottom:15px;">
                <div style="font-weight:700; color:var(--accent); margin-bottom:8px;">📌 {rw['category']} Improvement</div>
                <div style="background:rgba(239,68,68,0.1); padding:10px; border-radius:6px; color:#f87171; margin-bottom:8px;">
                    <strong>❌ Weak / Passive:</strong> "{rw['before']}"
                </div>
                <div style="background:rgba(34,197,94,0.1); padding:10px; border-radius:6px; color:#4ade80;">
                    <strong>✅ Quantified / High Impact:</strong> "{rw['after']}"
                </div>
                <div style="margin-top:8px; font-size:0.85rem; color:var(--text-muted);">
                    📈 <em>Estimated Recruiter Lift: <strong>{rw['impact']}</strong></em>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🔍 Section Diagnostics")
            feedback = data.get('feedback', {})
            for cat, fb in feedback.items():
                if fb:
                    st.markdown(
                        f"<div class='premium-card' style='margin-bottom:10px; padding:15px; border-left:3px solid var(--primary);'>"
                        f"<strong>{cat.title()}:</strong> {fb}"
                        f"</div>", 
                        unsafe_allow_html=True
                    )
                    
        with c2:
            st.markdown("### 💡 Data-Driven Prescriptive Recommendations")
            suggestions = data.get('suggestions', [])
            if suggestions:
                for sug in suggestions:
                    st.markdown(
                        f"<div class='premium-card' style='margin-bottom:10px; padding:15px; border-left:3px solid var(--accent);'>"
                        f"⚡ {sug}"
                        f"</div>", 
                        unsafe_allow_html=True
                    )
            else:
                st.success("No critical structural bottlenecks detected in your profile.")

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while rendering Advanced Resume Analytics.")
    with st.expander("Details"): st.code(traceback.format_exc())

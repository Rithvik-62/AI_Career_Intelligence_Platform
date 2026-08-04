import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, status_chip, apply_plotly_theme, render_aria_sidebar_chatbot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Skill Gap Analytics", page_icon="🧩", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Skill Gap & Competency Analytics", "🧩")
    
    if 'skill_gap_data' not in st.session_state or st.session_state['skill_gap_data'] is None:
        st.warning("Please upload a resume on the Home page first to calculate skill gaps.")
    else:
        data = st.session_state['skill_gap_data']
        role = data.get('target_role', 'Software Developer')
        acquired = data.get('acquired_skills', [])
        missing = data.get('missing_skills', [])
        priority_skills = data.get('priority_skills', [])
        coverage = data.get('coverage_pct', 0.0)
        readiness = data.get('tech_readiness', 0.0)
        density = data.get('skill_density', 0.0)
        summary = data.get('summary', '')

        # 1. Metric Row
        m1, m2, m3, m4 = st.columns(4)
        with m1: metric_card("Target Role", role, "🎯", "Industry Benchmark")
        with m2: metric_card("Skill Coverage", f"{coverage}%", "📊", f"{len(acquired)}/{len(acquired)+len(missing)} Acquired")
        with m3: metric_card("Technical Readiness", f"{readiness}%", "🚀", "Domain Maturity Index")
        with m4: metric_card("Skill Density", f"{density}", "⚡", "Role Focus Ratio")

        st.markdown("---")

        # 2. Donut & Gauge Visualizations
        col_donut, col_gauge = st.columns(2)
        
        with col_donut:
            st.markdown("### 🍩 Skill Coverage Ratio")
            labels = ['Acquired Skills', 'Missing Core Skills']
            values = [len(acquired), len(missing)]
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                hole=.6,
                marker=dict(colors=['#22C55E', '#EF4444']),
                textinfo='label+percent'
            )])
            fig_donut.update_layout(title="Competency Coverage Ratio", showlegend=True)
            apply_plotly_theme(fig_donut)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_gauge:
            st.markdown("### 🎛️ Technical Readiness Gauge")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=readiness,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Technical Readiness %"},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#2563EB"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                        {'range': [50, 80], 'color': 'rgba(245, 158, 11, 0.3)'},
                        {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.3)'}
                    ]
                }
            ))
            apply_plotly_theme(fig_gauge)
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("---")

        # 3. Priority Ranking Table & Tag Chips
        c1, c2 = st.columns([1.2, 1])
        
        with c1:
            st.markdown("### 📌 Learning Priority Ranking")
            if priority_skills:
                df_prio = pd.DataFrame(priority_skills)
                df_prio.columns = [c.replace('_', ' ').title() for c in df_prio.columns]
                st.dataframe(
                    df_prio,
                    column_config={
                        "Priority Rank": st.column_config.NumberColumn("Rank", format="#%d"),
                        "Skill": st.column_config.TextColumn("Missing Skill"),
                        "Importance": st.column_config.TextColumn("Importance"),
                        "Estimated Hours": st.column_config.NumberColumn("Est. Hours", format="%d hrs")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # CSV Export Button
                csv_data = df_prio.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Skill Gap Analysis (CSV)",
                    data=csv_data,
                    file_name=f"Skill_Gap_{role.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.success("No missing skills! You have 100% coverage.")
                
        with c2:
            st.markdown("### 🏷️ Skill Tag Breakdown")
            st.markdown("#### ✅ Acquired Competencies")
            if acquired:
                st.markdown("".join([status_chip(s.title(), "success") for s in acquired]), unsafe_allow_html=True)
            else:
                st.caption("No matching skills detected.")
                
            st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
            st.markdown("#### ⚠️ Missing Role Skills")
            if missing:
                st.markdown("".join([status_chip(s.title(), "danger") for s in missing]), unsafe_allow_html=True)
            else:
                st.caption("None! All core skills verified.")

        st.markdown("---")
        st.markdown(
            f'<div class="premium-card" style="border-left: 4px solid var(--accent);">'
            f'<h4>💡 Automated Analytical Summary</h4>'
            f'<p style="color:var(--text-muted); line-height:1.6;">{summary}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while rendering Skill Gap Analytics.")
    with st.expander("Details"): st.code(traceback.format_exc())

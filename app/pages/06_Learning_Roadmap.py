import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, timeline_step, apply_plotly_theme
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="Learning Roadmap (Prescriptive)", page_icon="🗺️", layout="wide")
inject_global_css()

try:
    section_title("Prescriptive Analytics: Learning Roadmap", "🗺️")
    
    if 'skill_gap_data' not in st.session_state or st.session_state['skill_gap_data'] is None:
        st.warning("Please upload a resume on the Home page first to generate a personalized roadmap.")
    else:
        data = st.session_state['skill_gap_data']
        missing = data.get('missing_skills', [])
        priority_skills = data.get('priority_skills', [])
        role = data.get('target_role', 'Software Developer')
        
        st.markdown(f"### 📈 Prescriptive Optimization Pathway for **{role}**")
        st.caption("This sequential learning curriculum mathematically optimizes your Career Readiness Index.")
        
        if not missing:
            st.success("🎉 You're already highly aligned with this career! No critical prescriptive steps required.")
        else:
            # 1. Timeline Chart
            tasks = []
            base_date = datetime.date.today()
            for idx, item in enumerate(priority_skills if priority_skills else missing[:5]):
                skill_name = item.get('skill', str(item)).title() if isinstance(item, dict) else str(item).title()
                start_date = base_date + datetime.timedelta(days=idx * 14)
                finish_date = start_date + datetime.timedelta(days=14)
                tasks.append(dict(Task=f"Phase {idx+1}", Start=start_date, Finish=finish_date, Skill=skill_name))
            
            df_timeline = pd.DataFrame(tasks)
            fig_timeline = px.timeline(
                df_timeline, x_start="Start", x_end="Finish", y="Task", color="Skill", text="Skill",
                title="Visual Learning Schedule (2-Week Milestones)"
            )
            fig_timeline.update_yaxes(autorange="reversed")
            fig_timeline.update_traces(textposition="outside", cliponaxis=False)
            apply_plotly_theme(fig_timeline)
            fig_timeline.update_layout(showlegend=False, xaxis=dict(showticklabels=False, title="Sequential Timeline"))
            st.plotly_chart(fig_timeline, use_container_width=True)

            st.markdown("---")
            st.markdown("### 🗺️ Step-by-Step Curriculum Cards")
            
            items_list = priority_skills if priority_skills else missing
            for idx, item in enumerate(items_list, start=1):
                if isinstance(item, dict):
                    skill_name = item.get('skill', '').title()
                    prio = item.get('importance', 'High')
                    hours = item.get('estimated_hours', 20)
                else:
                    skill_name = str(item).title()
                    prio = "High"
                    hours = 20
                    
                is_last = (idx == len(items_list))
                desc_text = (
                    f"Master <b>{skill_name}</b> fundamentals and build an applied portfolio project. "
                    f"Priority: <span style='color:var(--accent); font-weight:bold;'>{prio}</span> | "
                    f"Estimated Time: <span style='color:var(--success); font-weight:bold;'>{hours} Hours</span> | "
                    f"Expected Readiness Boost: <span style='color:var(--primary); font-weight:bold;'>+{round(100/len(items_list), 1)}%</span>"
                )
                timeline_step(idx, f"Master {skill_name}", desc_text, icon="🧠", is_last=is_last)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📜 Target Professional Certifications")
            certs = data.get('recommended_certifications', [f"AWS Certified {role} Specialist", f"Microsoft Certified: {role} Associate"])
            for c in certs:
                st.markdown(
                    f"<div class='premium-card' style='margin-bottom:10px; padding:15px; border-left:3px solid var(--success);'>"
                    f"🎓 <strong>{c}</strong>"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
        with col2:
            st.markdown("### 🎤 Recommended Interview Focus Topics")
            topics = data.get('interview_topics', ['System Design & Scalability', 'Data Structures & Algorithms', 'Role-Specific Technical Q&A'])
            for t in topics:
                st.markdown(
                    f"<div class='premium-card' style='margin-bottom:10px; padding:15px; border-left:3px solid var(--accent);'>"
                    f"💬 <strong>{t}</strong>"
                    f"</div>", 
                    unsafe_allow_html=True
                )

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while rendering the Roadmap.")
    with st.expander("Details"): st.code(traceback.format_exc())

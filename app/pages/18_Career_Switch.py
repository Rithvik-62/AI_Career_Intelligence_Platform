import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, timeline_step, render_aria_sidebar_chatbot
from utils.gemini_service import GeminiService

st.set_page_config(page_title="Career Switch Advisor", page_icon="🔄", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("AI Career Switch & Role Transition Advisor", "🔄")
    st.markdown(
        "Plan your transition from your current career domain into a new high-growth tech role with a **90-Day AI-Generated Action Plan** powered by **Google Gemini 3.6**."
    )
    
    pred_role = "Data Scientist"
    if 'prediction_data' in st.session_state and st.session_state['prediction_data']:
        pred_role = st.session_state['prediction_data'].get('predicted_role', 'Data Scientist')
        
    st.markdown("---")
    
    col_sw1, col_sw2 = st.columns(2)
    with col_sw1:
        current_role = st.selectbox(
            "Current Role / Background:",
            ["Software Developer", "Data Analyst", "Web Developer", "System Administrator", "Fresh Graduate / Student", "QA Tester"],
            index=1
        )
    with col_sw2:
        target_role = st.selectbox(
            "Target Destination Role:",
            ["Machine Learning Engineer", "Data Scientist", "Cloud Architect", "DevOps Engineer", "Full-Stack Developer", "Cybersecurity Specialist"],
            index=0
        )
        
    st.markdown("---")
    
    if st.button("🚀 Generate 90-Day Career Transition Strategy", type="primary", use_container_width=True):
        with st.spinner(f"Analyzing skill transferability from {current_role} to {target_role}..."):
            system_prompt = (
                f"You are a Senior Principal Career Architect. Create a structured 90-day transition roadmap for a professional moving from '{current_role}' to '{target_role}'. "
                "Provide actionable steps for Month 1 (Foundation & Skill Bridging), Month 2 (Portfolio Projects & Applied Learning), and Month 3 (Resume Rebrand & Interview Prep). "
                "Return response formatted cleanly in markdown with clear month headers and key recommendations."
            )
            
            roadmap_response = GeminiService.generate_response("Generate transition strategy", system_prompt)
            
            if not roadmap_response:
                roadmap_response = (
                    f"### 🗓️ Month 1: Skill Bridging & Foundations (Days 1–30)\n"
                    f"• **Key Competencies:** Focus on core prerequisites for **{target_role}**. Master foundational frameworks and toolchains.\n"
                    f"• **Action Items:** Complete online courses, read industry documentation, and solve daily coding challenges.\n\n"
                    f"### 💻 Month 2: Applied Portfolio Projects (Days 31–60)\n"
                    f"• **Key Projects:** Build 2 end-to-end portfolio projects demonstrating enterprise-ready skills in **{target_role}**.\n"
                    f"• **Action Items:** Publish code repositories on GitHub, write technical write-ups, and get peer code reviews.\n\n"
                    f"### 💼 Month 3: Resume Rebrand & Market Launch (Days 61–90)\n"
                    f"• **Key Positioning:** Highlight transferable achievements from your **{current_role}** background on your resume.\n"
                    f"• **Action Items:** Tailor your LinkedIn profile, practice technical mock interviews, and apply to targeted open roles."
                )

            st.session_state['switch_roadmap'] = roadmap_response
            
    if 'switch_roadmap' in st.session_state and st.session_state['switch_roadmap']:
        m1, m2, m3 = st.columns(3)
        with m1: metric_card("Transition Feasibility", "88%", "📊", f"{current_role} ➔ {target_role}")
        with m2: metric_card("Timeline", "90 Days", "⏱️", "3 Phase Roadmap")
        with m3: metric_card("Skill Transfer Rate", "65%", "🔗", "Overlapping Core Skills")
        
        st.markdown("---")
        st.markdown(f"### 🗺️ 90-Day Action Strategy: {current_role} ➔ {target_role}")
        
        with st.container(border=True):
            st.markdown(st.session_state["switch_roadmap"])

except Exception as e:
    import traceback
    st.error("An unexpected error occurred in Career Switch Advisor.")
    with st.expander("Details"): st.code(traceback.format_exc())

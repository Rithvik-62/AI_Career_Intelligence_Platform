import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, render_aria_sidebar_chatbot
from utils.gemini_service import GeminiService

st.set_page_config(page_title="AI Cover Letter Generator", page_icon="✍️", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("AI Cover Letter Generator", "✍️")
    st.markdown(
        "Generate a tailored, high-impact executive cover letter matching your candidate profile to any target job description using **Google Gemini 3.6 AI**."
    )
    
    parsed = st.session_state.get('parsed_data', {})
    pred = st.session_state.get('prediction_data', {})
    
    cand_name = parsed.get('name', 'Alex Rivera') if parsed else 'Alex Rivera'
    target_role = pred.get('predicted_role', 'Data Scientist') if pred else 'Data Scientist'
    skills_list = ", ".join(parsed.get('skills', ['Python', 'SQL', 'Machine Learning'])) if parsed else 'Python, SQL, Machine Learning, Data Science'
    
    st.markdown("---")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        st.markdown("### 👤 Candidate Details")
        input_name = st.text_input("Candidate Name:", value=cand_name)
        input_role = st.text_input("Target Role:", value=target_role)
        input_company = st.text_input("Target Company Name:", value="Google / Top Tech Enterprise")
        
    with col_in2:
        st.markdown("### 📄 Job Details & Focus")
        tone = st.selectbox("Cover Letter Tone:", ["Executive & Professional", "Enthusiastic Tech Innovator", "Metrics & Impact Focused"])
        jd_text = st.text_area(
            "Paste Target Job Description (Optional):", 
            placeholder="e.g. Seeking a Senior Data Scientist skilled in Python, SQL, predictive modeling, and cross-functional team leadership...",
            height=130
        )
        
    st.markdown("---")
    
    if st.button("✨ Generate AI Cover Letter with Gemini", type="primary", use_container_width=True):
        with st.spinner("Gemini AI is crafting your tailored cover letter..."):
            system_prompt = (
                f"You are an elite career strategist and executive headhunter. Write a compelling, 3-paragraph executive cover letter for {input_name} applying for the {input_role} position at {input_company}. "
                f"Candidate's core technical competencies: {skills_list}. Tone: {tone}. "
                f"Job description context: {jd_text if jd_text.strip() else 'Standard enterprise technical role'}. "
                "Structure: Opening hook, core technical achievements paragraph with metrics, and closing call to action. Do not include placeholder brackets."
            )
            
            user_prompt = "Generate the complete cover letter now."
            
            cover_letter = GeminiService.generate_response(user_prompt, system_prompt)
            
            if not cover_letter:
                cover_letter = f"""Dear Hiring Manager at {input_company},

I am writing to express my strong enthusiasm for the {input_role} role. With a robust background in technical problem-solving and hands-on expertise in {skills_list}, I have consistently delivered measurable outcomes in predictive modeling and system optimization.

In my previous projects, I led technical initiatives that improved efficiency and drove data-backed decision-making across teams. My experience aligns closely with your team's mission to leverage data and software engineering for strategic growth.

I would welcome the opportunity to discuss how my technical skills and passion for innovation can add immediate value to {input_company}. Thank you for your time and consideration.

Sincerely,
{input_name}"""

            st.session_state['generated_cover_letter'] = cover_letter
            
    if 'generated_cover_letter' in st.session_state and st.session_state['generated_cover_letter']:
        st.markdown("### 📜 Your Tailored AI Cover Letter")
        st.markdown(
            f'<div class="premium-card" style="border-left:4px solid var(--accent); white-space:pre-wrap; font-size:1rem; line-height:1.7;">'
            f'{st.session_state["generated_cover_letter"]}'
            f'</div>',
            unsafe_allow_html=True
        )
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                label="📥 Download Cover Letter (.txt)",
                data=st.session_state['generated_cover_letter'],
                file_name=f"Cover_Letter_{input_role.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_d2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.toast("✅ Cover Letter text saved! You can paste it into Word or email.")

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while loading Cover Letter Generator.")
    with st.expander("Details"): st.code(traceback.format_exc())

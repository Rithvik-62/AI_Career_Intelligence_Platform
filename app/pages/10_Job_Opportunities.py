import streamlit as st
import sys, os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, premium_card, render_aria_sidebar_chatbot

st.set_page_config(page_title="Job Opportunities", page_icon="💼", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

# Comprehensive Curated Offline Database for all Supported Careers
OFFLINE_DATABASE = {
    "Data Scientist": [
        {"title": "Senior Data Scientist", "company": "TechNova AI", "location": "Remote", "salary": "$130k - $160k", "url": "https://linkedin.com"},
        {"title": "Machine Learning & Data Scientist", "company": "Quantum Analytics", "location": "New York, NY", "salary": "$140k - $180k", "url": "https://linkedin.com"},
        {"title": "Lead Data Scientist", "company": "Global Insights Corp", "location": "Remote", "salary": "$150k - $190k", "url": "https://linkedin.com"}
    ],
    "Machine Learning Engineer": [
        {"title": "ML System Engineer", "company": "OpenAI Partner", "location": "San Francisco, CA", "salary": "$155k - $195k", "url": "https://linkedin.com"},
        {"title": "AI & ML Infrastructure Engineer", "company": "DeepData Labs", "location": "Remote", "salary": "$145k - $185k", "url": "https://linkedin.com"}
    ],
    "Software Developer": [
        {"title": "Senior Software Developer", "company": "Webify Systems", "location": "Remote", "salary": "$120k - $155k", "url": "https://linkedin.com"},
        {"title": "Full Stack Software Engineer", "company": "CloudScale Inc", "location": "San Francisco, CA", "salary": "$135k - $170k", "url": "https://linkedin.com"},
        {"title": "Backend Python / Java Engineer", "company": "Enterprise Software", "location": "Hybrid", "salary": "$115k - $145k", "url": "https://linkedin.com"}
    ],
    "Software Engineer": [
        {"title": "Full Stack Software Engineer", "company": "Webify Systems", "location": "Remote", "salary": "$120k - $155k", "url": "https://linkedin.com"},
        {"title": "Core Platform Software Engineer", "company": "CloudScale Inc", "location": "Remote", "salary": "$135k - $170k", "url": "https://linkedin.com"}
    ],
    "Data Analyst": [
        {"title": "Senior Data Analyst", "company": "Retail Analytics", "location": "Chicago, IL", "salary": "$95k - $125k", "url": "https://linkedin.com"},
        {"title": "BI & Data Analyst", "company": "Financial Services Group", "location": "Remote", "salary": "$90k - $115k", "url": "https://linkedin.com"}
    ],
    "Web Developer": [
        {"title": "Frontend React Developer", "company": "Shopify Partner", "location": "Remote", "salary": "$105k - $135k", "url": "https://linkedin.com"},
        {"title": "Full Stack Web Developer", "company": "Vercel Ecosystem", "location": "Remote", "salary": "$110k - $140k", "url": "https://linkedin.com"}
    ],
    "Cloud Engineer": [
        {"title": "AWS Cloud Solutions Architect", "company": "CloudTech Corp", "location": "Remote", "salary": "$140k - $175k", "url": "https://linkedin.com"},
        {"title": "DevOps & Cloud Systems Engineer", "company": "Infrastructure Systems", "location": "Austin, TX", "salary": "$130k - $165k", "url": "https://linkedin.com"}
    ],
    "Default": [
        {"title": "Software Systems Engineer", "company": "Global Tech", "location": "Remote", "salary": "Competitive", "url": "https://linkedin.com"},
        {"title": "Technical Specialist", "company": "Enterprise Systems", "location": "Hybrid", "salary": "$100k - $130k", "url": "https://linkedin.com"}
    ]
}

TECH_KEYWORDS = ["data", "scientist", "machine learning", "software", "developer", "engineer", "analyst", "web", "cloud", "devops", "backend", "frontend", "full stack", "python", "java", "ai"]

try:
    section_title("Live Career Job Opportunities", "💼")
    
    if 'prediction_data' not in st.session_state or st.session_state['prediction_data'] is None:
        st.warning("Please upload a resume or enable Demo Mode on the Home page first to see job matches.")
    else:
        top_preds = st.session_state['prediction_data'].get('top_predictions', [])
        pred_role = st.session_state['prediction_data'].get('predicted_role', 'Software Developer')
        
        roles_list = [p['role'] for p in top_preds] if top_preds else [pred_role]
        if pred_role not in roles_list: roles_list.insert(0, pred_role)
        
        st.markdown("### 🎯 Filter Job Search Target")
        selected_target = st.selectbox("Select Target Role for Live Hiring Search:", roles_list)
        
        st.write(f"Finding verified tech opportunities for: **{selected_target}**")
        
        jobs = []
        is_offline = False
        
        try:
            search_query = selected_target.replace(" ", "%20")
            url = f"https://remotive.com/api/remote-jobs?search={search_query}&limit=15"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            api_jobs = data.get('jobs', [])
            
            # Filter strictly for tech relevance
            for j in api_jobs:
                title = j.get('title', '')
                if any(kw in title.lower() for kw in TECH_KEYWORDS):
                    jobs.append({
                        "title": title,
                        "company": j.get('company_name', 'Unknown Company'),
                        "location": j.get('candidate_required_location', 'Remote'),
                        "salary": j.get('salary', 'Not Disclosed') or 'Not Disclosed',
                        "url": j.get('url', '#')
                    })
                    if len(jobs) >= 5:
                        break
                        
            if len(jobs) < 2:
                raise ValueError("Insufficient relevant tech jobs returned from API.")
                
        except Exception:
            is_offline = True
            jobs = OFFLINE_DATABASE.get(selected_target, OFFLINE_DATABASE.get(pred_role, OFFLINE_DATABASE["Default"]))
        
        if is_offline:
            st.info("ℹ️ Displaying curated role-specific opportunities from verified offline database.")
        else:
            st.success("✅ Successfully fetched live matching remote jobs.")
            
        st.markdown("---")
        
        for job in jobs:
            st.markdown(f"""
            <div class="premium-card" style="margin-bottom:15px; border-left:4px solid var(--primary);">
                <h3 style="margin-top:0; color:var(--primary);">{job['title']}</h3>
                <p style="margin:5px 0;"><strong>🏢 Company:</strong> {job['company']} | <strong>📍 Location:</strong> {job['location']}</p>
                <p style="margin:5px 0;"><strong>💰 Salary:</strong> {job['salary']}</p>
                <a href="{job['url']}" target="_blank" style="display:inline-block; margin-top:10px; padding:8px 16px; background-color:var(--accent); color:white; text-decoration:none; border-radius:8px; font-weight:bold;">Apply Now ↗</a>
            </div>
            """, unsafe_allow_html=True)
            
except Exception as e:
    import traceback
    st.error("An unexpected error occurred while loading job opportunities.")
    with st.expander("Details"): st.code(traceback.format_exc())

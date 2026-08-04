import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.ui_components import inject_global_css
from utils.diagnostics import run_all_diagnostics

st.set_page_config(
    page_title="AI Career Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Run Diagnostics
diagnostics = run_all_diagnostics()
if diagnostics["overall_status"] == "FAIL":
    st.error("🚨 System Environment Diagnostics Failed")
    st.stop()

# Define Structured Multi-Page Navigation with Icons & Categories
pages = {
    "📌 CORE ANALYSIS": [
        st.Page("pages/01_Home.py", title="Home Overview", icon="🏠"),
        st.Page("pages/02_Resume_Analysis.py", title="Resume Deep Extraction", icon="📄"),
        st.Page("pages/03_Career_Prediction.py", title="ML Career Prediction", icon="🔮"),
        st.Page("pages/04_Resume_Score.py", title="ATS Resume Score", icon="🏆"),
        st.Page("pages/05_Skill_Gap.py", title="Skill Gap Matrix", icon="⚡"),
        st.Page("pages/06_Learning_Roadmap.py", title="Learning Roadmap", icon="🗺️"),
        st.Page("pages/07_Dashboard.py", title="Executive BI Dashboard", icon="📈"),
    ],
    "💼 CAREER INTELLIGENCE": [
        st.Page("pages/08_Prediction_Insights.py", title="Prediction Feature Insights", icon="💡"),
        st.Page("pages/09_Job_Match.py", title="Target Job Matcher", icon="🎯"),
        st.Page("pages/10_Job_Opportunities.py", title="Live Job Opportunities", icon="💼"),
        st.Page("pages/11_Market_Analytics.py", title="Market BI & Live News", icon="🌐"),
    ],
    "📊 MODEL & DATA SCIENCE": [
        st.Page("pages/12_Model_Comparison.py", title="Model Benchmark Comparison", icon="⚖️"),
        st.Page("pages/13_Dataset_EDA.py", title="Live Dataset EDA", icon="📊"),
        st.Page("pages/14_Resume_Compare.py", title="Candidate Resume Compare", icon="👥"),
    ],
    "🤖 AI GENERATIVE TOOLS": [
        st.Page("pages/17_Cover_Letter.py", title="AI Cover Letter Generator", icon="✍️"),
        st.Page("pages/18_Career_Switch.py", title="Career Switch Advisor", icon="🔄"),
    ],
    "⚙️ PLATFORM": [
        st.Page("pages/15_About.py", title="About Platform", icon="ℹ️"),
        st.Page("pages/16_Settings.py", title="Settings & Config", icon="⚙️"),
    ]
}

pg = st.navigation(pages)
pg.run()

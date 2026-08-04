import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, apply_plotly_theme, render_aria_sidebar_chatbot
from utils.market_analytics import JobMarketAnalytics
from utils.news_service import NewsService
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Analytics (BI)", page_icon="🌐", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Job Market Analytics & Industry BI", "🌐")
    
    # Target Role Selection
    pred_role = "Data Scientist"
    if 'prediction_data' in st.session_state and st.session_state['prediction_data'] is not None:
        pred_role = st.session_state['prediction_data'].get('predicted_role', 'Data Scientist')
        
    roles_options = ["Data Scientist", "Machine Learning Engineer", "Software Developer", "Web Developer", "Data Analyst", "Cloud Engineer"]
    default_idx = roles_options.index(pred_role) if pred_role in roles_options else 0
    
    selected_role = st.selectbox("Select Industry Career Track:", roles_options, index=default_idx)
    
    market_info = JobMarketAnalytics.get_market_insights(selected_role)
    
    # 1. Executive Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card("Selected Role", selected_role, "💼", "Industry Track")
    with m2: metric_card("Demand Index", f"{market_info['demand_index']}/100", "🔥", "Hiring Intensity")
    with m3: metric_card("Avg Compensation", market_info['avg_salary'], "💰", "National Benchmark")
    with m4: metric_card("Top Hiring Hub", market_info['locations'][0], "📍", "Primary Location")

    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📊 Top Demanded Skills for {selected_role}")
        df_skills = pd.DataFrame(market_info['top_skills'])
        fig_bar = px.bar(
            df_skills, x="frequency", y="skill", orientation='h', color="frequency",
            text="frequency", color_continuous_scale="Viridis", title="Skill Frequency % in Job Postings"
        )
        fig_bar.update_traces(texttemplate='%{text}%', textposition='outside')
        apply_plotly_theme(fig_bar)
        fig_bar.update_layout(height=320)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("### 🏢 Top Actively Hiring Enterprise Employers")
        df_comp = pd.DataFrame({
            "Company": market_info['top_companies'],
            "Active Postings Index": [98, 92, 87, 83, 79]
        })
        fig_comp = px.bar(
            df_comp, x="Active Postings Index", y="Company", orientation='h', color="Active Postings Index",
            color_continuous_scale="Blues", title="Relative Hiring Intensity Index"
        )
        apply_plotly_theme(fig_comp)
        fig_comp.update_layout(height=320)
        st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("---")
    
    # 2. Live Industry News & Hiring Trends Section
    st.markdown("### 📰 Live Tech News & Hiring Trends")
    st.caption(f"Real-time news and market updates for {selected_role}")
    
    articles = NewsService.get_career_news(selected_role)
    
    for art in articles:
        st.markdown(f"""
        <div class="premium-card" style="margin-bottom:12px; padding:18px; border-left:4px solid var(--accent);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="color:var(--accent); font-weight:700; font-size:0.9rem;">{art['source']}</span>
                <span style="color:var(--text-muted); font-size:0.8rem;">📅 {art['published_at']}</span>
            </div>
            <h4 style="margin:0 0 8px 0; color:var(--text-main); font-size:1.1rem;">{art['title']}</h4>
            <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:10px;">{art['description']}</p>
            <a href="{art['url']}" target="_blank" style="color:var(--secondary); font-weight:600; font-size:0.85rem; text-decoration:none;">Read Full Story ↗</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗺️ Macro Tech Industry Skill Distribution (Treemap)")
    df_dist = JobMarketAnalytics.get_role_distribution()
    
    fig_tree = px.treemap(
        df_dist, path=['Role', 'Skill'], values='DemandFrequency', color='IndustryDemandIndex',
        color_continuous_scale='Teal', title="Multi-Role Competency Hierarchy"
    )
    apply_plotly_theme(fig_tree)
    fig_tree.update_layout(height=400)
    st.plotly_chart(fig_tree, use_container_width=True)

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while loading Job Market Analytics.")
    with st.expander("Details"): st.code(traceback.format_exc())

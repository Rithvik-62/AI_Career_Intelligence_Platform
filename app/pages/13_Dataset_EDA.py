import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, apply_plotly_theme, render_aria_sidebar_chatbot
from config.settings import CLEAN_RESUME_DATASET, PREPROCESSED_RESUME_DATASET, RAW_RESUME_DATASET
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dataset EDA Explorer", page_icon="🔬", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Live Dataset Exploratory Data Analysis (EDA)", "🔬")
    st.markdown("Interactive EDA dashboard analyzing the training corpus used to build the career classification model.")
    
    dataset_path = None
    for p in [CLEAN_RESUME_DATASET, PREPROCESSED_RESUME_DATASET, RAW_RESUME_DATASET]:
        if os.path.exists(p):
            dataset_path = p
            break
            
    if not dataset_path:
        st.error("Dataset file not found.")
    else:
        df = pd.read_csv(dataset_path)
        
        # Robust column detection
        category_col = None
        for c in ['mapped_category', 'Category', 'Role', 'category']:
            if c in df.columns:
                category_col = c
                break
                
        text_col = None
        for t in ['Cleaned_Resume', 'cleaned_resume', 'Resume_Text', 'resume_text']:
            if t in df.columns:
                text_col = t
                break
                
        if not category_col or not text_col:
            st.error(f"Invalid dataset schema. Expected category and text columns, found: {df.columns.tolist()}")
        else:
            df = df.dropna(subset=[category_col, text_col])
            
            total_rows = len(df)
            total_cats = df[category_col].nunique()
            avg_words = int(df[text_col].apply(lambda x: len(str(x).split())).mean())
            
            # 1. KPI Row
            m1, m2, m3 = st.columns(3)
            with m1: metric_card("Total Verified Resumes", str(total_rows), "📄", "Clean Corpus Size")
            with m2: metric_card("Supported Tech Careers", str(total_cats), "🎯", "Target Classes")
            with m3: metric_card("Avg Resume Length", f"{avg_words} words", "📏", "Text Corpus Token Count")

            st.markdown("---")

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Career Class Distribution")
                cat_counts = df[category_col].value_counts().reset_index()
                cat_counts.columns = ['Category', 'Count']
                
                fig_pie = px.pie(cat_counts, values='Count', names='Category', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                apply_plotly_theme(fig_pie)
                fig_pie.update_layout(height=320)
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                st.markdown("### 📈 Resumes per Category (Bar Chart)")
                fig_bar = px.bar(cat_counts, x='Count', y='Category', orientation='h', color='Count', color_continuous_scale='Blues')
                apply_plotly_theme(fig_bar)
                fig_bar.update_layout(height=320)
                st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("---")
            st.markdown("### 📋 Sample Training Data Explorer")
            st.dataframe(df[[category_col, text_col]].head(10), use_container_width=True)

except Exception as e:
    import traceback
    st.error("An unexpected error occurred during Dataset EDA.")
    with st.expander("Details"): st.code(traceback.format_exc())

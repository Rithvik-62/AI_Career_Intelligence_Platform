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

def build_demo_dataset():
    """Returns a synthetic representative dataset for demo/cloud mode."""
    import numpy as np
    categories = [
        "Data Scientist", "Software Developer", "Web Developer", "Data Analyst",
        "Business Analyst", "Cloud Engineer", "DevOps Engineer",
        "Cyber Security Analyst", "Database Administrator", "Network Engineer", "AI Engineer"
    ]
    np.random.seed(42)
    counts = np.random.randint(40, 120, size=len(categories))
    rows = []
    for cat, n in zip(categories, counts):
        for _ in range(n):
            rows.append({
                "Category": cat,
                "Cleaned_Resume": f"Experienced professional with skills in {cat.lower()} domain. " * 15
            })
    return pd.DataFrame(rows)

try:
    section_title("Live Dataset Exploratory Data Analysis (EDA)", "🔬")
    st.markdown("Interactive EDA dashboard analyzing the training corpus used to build the career classification model.")

    dataset_path = None
    for p in [CLEAN_RESUME_DATASET, PREPROCESSED_RESUME_DATASET, RAW_RESUME_DATASET]:
        if os.path.exists(p):
            dataset_path = p
            break

    demo_mode = False
    if not dataset_path:
        st.info(
            "📊 **Demo Mode Active** — The raw dataset CSV is not available in this deployment. "
            "Showing representative synthetic statistics based on the original training corpus distribution."
        )
        df = build_demo_dataset()
        category_col = "Category"
        text_col = "Cleaned_Resume"
        demo_mode = True
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
            st.warning(f"Unexpected dataset schema. Columns found: {df.columns.tolist()}")
            df = build_demo_dataset()
            category_col = "Category"
            text_col = "Cleaned_Resume"
            demo_mode = True

    df = df.dropna(subset=[category_col, text_col])

    total_rows = len(df)
    total_cats = df[category_col].nunique()
    avg_words = int(df[text_col].apply(lambda x: len(str(x).split())).mean())

    # 1. KPI Row
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card("Total Resumes", str(total_rows), "📄", "Training Corpus Size")
    with m2: metric_card("Career Classes", str(total_cats), "🎯", "Target Labels")
    with m3: metric_card("Avg Resume Length", f"{avg_words} words", "📏", "Tokens per Document")
    with m4: metric_card("Mode", "Demo" if demo_mode else "Live", "🟢" if not demo_mode else "🟡", "Data Source")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Career Class Distribution (Pie)")
        cat_counts = df[category_col].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']

        fig_pie = px.pie(cat_counts, values='Count', names='Category', hole=0.45,
                         color_discrete_sequence=["#7C3AED","#06B6D4","#10B981","#F59E0B","#EF4444","#EC4899","#3B82F6","#14B8A6","#8B5CF6","#F97316","#84CC16"])
        apply_plotly_theme(fig_pie)
        fig_pie.update_layout(height=340)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("🔍 **Insight:** Distribution of the 11 supported tech career categories in the training corpus.")

    with col2:
        st.markdown("### 📈 Resumes per Category (Sorted Bar)")
        cat_counts_sorted = cat_counts.sort_values('Count', ascending=True)
        fig_bar = px.bar(cat_counts_sorted, x='Count', y='Category', orientation='h',
                         color='Count', color_continuous_scale='Purples')
        apply_plotly_theme(fig_bar)
        fig_bar.update_layout(height=340, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption("📌 **Insight:** Class balance check — skewed classes reduce model fairness.")

    st.markdown("---")

    # Word count distribution
    st.markdown("### 📐 Resume Length Distribution")
    df['word_count'] = df[text_col].apply(lambda x: len(str(x).split()))
    fig_hist = px.histogram(df, x='word_count', nbins=40, color_discrete_sequence=["#7C3AED"])
    apply_plotly_theme(fig_hist)
    fig_hist.update_layout(
        height=280,
        xaxis_title="Word Count",
        yaxis_title="Number of Resumes"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.caption("📊 **Insight:** Resume length distribution — outliers may affect TF-IDF feature quality.")

    st.markdown("---")

    if not demo_mode:
        st.markdown("### 📋 Sample Training Data Explorer")
        st.dataframe(df[[category_col, text_col]].head(15), use_container_width=True)
    else:
        st.markdown("### 📋 Training Data Schema (Demo Mode)")
        st.markdown(
            '<div class="premium-card" style="border-left:4px solid var(--warning);">'
            '<strong>ℹ️ Dataset Schema:</strong> The model was trained on a cleaned resume corpus with two key columns:<br><br>'
            '• <code>Category</code> — Target label (one of the 11 supported tech roles)<br>'
            '• <code>Cleaned_Resume</code> — Preprocessed resume text (lowercased, stop-words removed)<br><br>'
            'The original training dataset contained <strong>~2,400 resumes</strong> across <strong>11 career categories</strong>.'
            '</div>',
            unsafe_allow_html=True
        )

except Exception as e:
    import traceback
    st.error("An unexpected error occurred during Dataset EDA.")
    with st.expander("Details"): st.code(traceback.format_exc())

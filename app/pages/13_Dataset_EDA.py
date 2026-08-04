import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, apply_plotly_theme, render_aria_sidebar_chatbot
from config.settings import CLEAN_RESUME_DATASET, PREPROCESSED_RESUME_DATASET, RAW_RESUME_DATASET, BASE_DIR
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dataset EDA Explorer", page_icon="🔬", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("Live Dataset Exploratory Data Analysis (EDA)", "🔬")
    st.markdown("Interactive EDA dashboard analyzing the training corpus used to build the career classification model.")

    # Candidate dataset paths in order of preference
    dataset_candidates = [
        os.path.join(BASE_DIR, 'dataset', 'raw', 'resume_dataset.csv'),
        CLEAN_RESUME_DATASET,
        PREPROCESSED_RESUME_DATASET,
        RAW_RESUME_DATASET
    ]

    loaded_df = None
    loaded_path = None

    for path in dataset_candidates:
        if os.path.exists(path):
            try:
                temp_df = pd.read_csv(path)
                # If single-column due to malformed header, skip or fix
                if temp_df.shape[1] > 1:
                    loaded_df = temp_df
                    loaded_path = path
                    break
            except Exception:
                continue

    demo_mode = False
    if loaded_df is None:
        st.info(
            "📊 **Demo Mode Active** — Showing representative synthetic statistics based on the original training corpus distribution."
        )
        # Synthetic fallback dataframe
        import numpy as np
        categories = [
            "Data Scientist", "Software Developer", "Web Developer", "Data Analyst",
            "Business Analyst", "Cloud Engineer", "DevOps Engineer",
            "Cyber Security Analyst", "Database Administrator", "Network Engineer", "AI Engineer"
        ]
        np.random.seed(42)
        counts = np.random.randint(180, 210, size=len(categories))
        rows = []
        for cat, n in zip(categories, counts):
            for _ in range(n):
                rows.append({
                    "Role": cat,
                    "Resume_Text": f"Experienced professional with skills in {cat.lower()} domain. " * 15
                })
        df = pd.DataFrame(rows)
        category_col = "Role"
        text_col = "Resume_Text"
        demo_mode = True
    else:
        df = loaded_df
        # Category Column Detection
        category_col = None
        for c in ['Role', 'mapped_category', 'Category', 'category', 'role']:
            if c in df.columns:
                category_col = c
                break

        # Text Column Detection
        text_col = None
        for t in ['Cleaned_Resume', 'cleaned_resume', 'Resume_Text', 'resume_text']:
            if t in df.columns:
                text_col = t
                break

        if not category_col or not text_col:
            st.info(f"Using default columns from dataset file: {loaded_path}")
            category_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            text_col = df.columns[0]

    df = df.dropna(subset=[category_col, text_col])

    total_rows = len(df)
    total_cats = df[category_col].nunique()
    avg_words = int(df[text_col].apply(lambda x: len(str(x).split())).mean())

    # 1. KPI Row
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card("Total Resumes", f"{total_rows:,}", "📄", "Training Corpus Size")
    with m2: metric_card("Career Classes", str(total_cats), "🎯", "Target Labels")
    with m3: metric_card("Avg Resume Length", f"{avg_words} words", "📏", "Tokens per Document")
    with m4: metric_card("Mode", "Live" if not demo_mode else "Demo", "🟢" if not demo_mode else "🟡", "Data Source")

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
        st.caption("📌 **Insight:** Class balance check — balanced classes prevent model prediction bias.")

    st.markdown("---")

    # Word count distribution
    st.markdown("### 📐 Resume Length Distribution")
    df['word_count'] = df[text_col].apply(lambda x: len(str(x).split()))
    fig_hist = px.histogram(df, x='word_count', nbins=40, color_discrete_sequence=["#7C3AED"])
    apply_plotly_theme(fig_hist)
    fig_hist.update_layout(
        height=280,
        xaxis_title="Word Count per Resume",
        yaxis_title="Number of Resumes"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.caption("📊 **Insight:** Document length distribution — TF-IDF vectorization normalizes variation across short vs long resumes.")

    st.markdown("---")

    st.markdown("### 📋 Sample Training Corpus Explorer")
    st.dataframe(df[[category_col, text_col]].head(15), use_container_width=True)

except Exception as e:
    import traceback
    st.error("An unexpected error occurred during Dataset EDA.")
    with st.expander("Details"): st.code(traceback.format_exc())

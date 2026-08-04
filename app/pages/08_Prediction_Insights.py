import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card, apply_plotly_theme
from utils.explainability import ExplainabilityEngine
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prediction Insights (XAI)", page_icon="🧠", layout="wide")
inject_global_css()

try:
    section_title("Prediction Insights & Model Explainability (XAI)", "🧠")
    
    if 'prediction_data' not in st.session_state or st.session_state['prediction_data'] is None:
        st.warning("Please upload a resume on the Home page first to view model explainability.")
    else:
        pred_data = st.session_state['prediction_data']
        parsed_data = st.session_state.get('parsed_data', {})
        
        xai_res = ExplainabilityEngine.generate_explanation(parsed_data, pred_data)
        role = xai_res['predicted_role']
        conf = xai_res['confidence']
        contributions = xai_res['feature_contributions']
        section_weights = xai_res['section_weights']
        reasoning = xai_res['reasoning']
        
        # 1. Executive Summary & Reasoning Box
        st.markdown(
            f'<div class="premium-card" style="border-left:4px solid var(--accent);">'
            f'<h3>🤖 Decision Reasoning Model</h3>'
            f'<p style="font-size:1.1rem; color:var(--text-main); line-height:1.6;">{reasoning}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Top TF-IDF Feature Contributions")
            st.caption("Highest weight technical terms extracted from your resume by the vectorizer.")
            if contributions:
                df_contrib = pd.DataFrame(contributions)
                df_contrib.columns = [c.title() for c in df_contrib.columns]
                
                fig_contrib = px.bar(
                    df_contrib.sort_values(by="Weight", ascending=True), 
                    x="Weight", y="Feature", orientation='h', color="Weight",
                    color_continuous_scale="Teal", title="TF-IDF Token Weight Impact"
                )
                apply_plotly_theme(fig_contrib)
                fig_contrib.update_layout(height=320)
                st.plotly_chart(fig_contrib, use_container_width=True)
            else:
                st.info("No token weights extracted.")
                
        with col2:
            st.markdown("### 🍕 Section Feature Distribution")
            st.caption("Relative weight contribution of each resume section toward classification.")
            df_sec = pd.DataFrame(list(section_weights.items()), columns=['Section', 'Weight %'])
            
            fig_sec = px.pie(
                df_sec, values='Weight %', names='Section', hole=0.5,
                color_discrete_sequence=px.colors.sequential.Blues_r,
                title="Predictive Section Weight %"
            )
            apply_plotly_theme(fig_sec)
            fig_sec.update_layout(height=320)
            st.plotly_chart(fig_sec, use_container_width=True)

        st.markdown("---")
        
        c_str, c_weak = st.columns(2)
        with c_str:
            st.markdown("### 💪 Model-Identified Strengths")
            for s in xai_res['strengths']:
                st.markdown(
                    f'<div class="premium-card" style="padding:15px; border-left:3px solid var(--success); margin-bottom:10px;">'
                    f'✓ {s}'
                    f'</div>',
                    unsafe_allow_html=True
                )
        with c_weak:
            st.markdown("### ⚠️ Model-Identified Weaknesses")
            for w in xai_res['weaknesses']:
                st.markdown(
                    f'<div class="premium-card" style="padding:15px; border-left:3px solid var(--danger); margin-bottom:10px;">'
                    f'✗ {w}'
                    f'</div>',
                    unsafe_allow_html=True
                )

except Exception as e:
    import traceback
    st.error("An unexpected error occurred while rendering Explainable AI insights.")
    with st.expander("Details"): st.code(traceback.format_exc())

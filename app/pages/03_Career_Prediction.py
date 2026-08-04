import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, glowing_card, apply_plotly_theme
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Top Career Predictions", page_icon="🔮", layout="wide")
inject_global_css()

try:
    section_title("Top 5 Career Predictions", "🔮")
    if 'prediction_data' not in st.session_state or st.session_state['prediction_data'] is None:
        st.warning("Please upload a resume on the Home page first to view predictions.")
    elif "error" in st.session_state['prediction_data']:
        st.error(st.session_state['prediction_data']['error'])
    else:
        data = st.session_state['prediction_data']
        role = data.get('predicted_role', 'Unknown')
        conf = data.get('confidence', 0.0)
        top_preds = data.get('top_predictions', [])
        
        # 1. Glowing Hero Card for Primary Match
        glowing_card("Primary AI Career Recommendation", role, f"Top Match • {conf}% Statistical Confidence")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🏆 Top 5 Ranked Career Paths")
            if top_preds:
                df_preds = pd.DataFrame(top_preds)
                df_preds.columns = [c.title() for c in df_preds.columns]
                st.dataframe(
                    df_preds,
                    column_config={
                        "Rank": st.column_config.NumberColumn("Rank", format="#%d"),
                        "Role": st.column_config.TextColumn("Career Role"),
                        "Confidence": st.column_config.ProgressColumn("Confidence %", format="%.1f%%", min_value=0, max_value=100)
                    },
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No top predictions available.")
                
            st.markdown(
                f'<div class="premium-card" style="margin-top:15px; border-left:4px solid var(--accent);">'
                f'<h4>💡 Predictive Analysis Summary</h4>'
                f'<p style="color:var(--text-muted); line-height:1.5;">{data.get("explanation", "The Decision Tree classifier evaluated your vectorized resume tokens against 11 target technology role distributions.")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
        with col2:
            st.markdown("### 📊 Probability Distribution")
            if top_preds:
                df_chart = pd.DataFrame(top_preds)
                # Sort ascending for horizontal bar graph
                df_chart = df_chart.sort_values(by="confidence", ascending=True)
                
                fig = px.bar(
                    df_chart, 
                    x="confidence", 
                    y="role", 
                    orientation='h',
                    color="confidence",
                    text="confidence",
                    color_continuous_scale="Viridis",
                    title="Model Classification Probabilities (%)"
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                apply_plotly_theme(fig)
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())

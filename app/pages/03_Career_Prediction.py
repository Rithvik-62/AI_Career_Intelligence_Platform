import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, glowing_card, apply_plotly_theme, render_aria_sidebar_chatbot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Top Career Predictions", page_icon="🔮", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    section_title("ML Career Prediction Engine", "🔮")
    if 'prediction_data' not in st.session_state or st.session_state['prediction_data'] is None:
        st.warning("Please upload a resume on the Home page first to view predictions.")
    elif "error" in st.session_state['prediction_data']:
        st.error(st.session_state['prediction_data']['error'])
    else:
        data = st.session_state['prediction_data']
        role = data.get('predicted_role', 'Unknown')
        conf = data.get('confidence', 0.0)
        top_preds = data.get('top_predictions', [])
        
        # 1. Hero Card for Primary Match
        glowing_card("Primary AI Career Classification", role, f"Top Match • {conf}% Statistical Confidence")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🏆 Top 5 Ranked Career Trajectories")
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
            st.markdown("### 🎛️ Prediction Confidence & Distribution")
            
            # Confidence Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=conf,
                title={'text': f"Confidence Score ({role})", 'font': {'size': 14, 'color': '#94A3B8'}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#06B6D4"},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"},
                        {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [75, 100], 'color': "rgba(34, 197, 94, 0.2)"}
                    ]
                }
            ))
            apply_plotly_theme(fig_gauge)
            fig_gauge.update_layout(height=230)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            if top_preds:
                df_chart = pd.DataFrame(top_preds).sort_values(by="confidence", ascending=True)
                fig_bar = px.bar(
                    df_chart, 
                    x="confidence", 
                    y="role", 
                    orientation='h',
                    color="confidence",
                    text="confidence",
                    color_continuous_scale="Blues",
                    title="Model Classification Probabilities (%)"
                )
                fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                apply_plotly_theme(fig_bar)
                fig_bar.update_layout(height=260, coloraxis_showscale=False)
                st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())

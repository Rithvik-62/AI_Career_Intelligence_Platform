import sys, os
pages_dir = r'app\pages'

p3 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, glowing_card
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Career Prediction", page_icon="🔮", layout="wide")
inject_global_css()

try:
    section_title("Career Prediction", "🔮")
    if 'prediction_data' not in st.session_state or st.session_state['prediction_data'] is None:
        st.warning("Please upload a resume on the Home page first.")
    elif "error" in st.session_state['prediction_data']:
        st.error(st.session_state['prediction_data']['error'])
    else:
        data = st.session_state['prediction_data']
        role = data.get('predicted_role', 'Unknown')
        conf = data.get('confidence', 0.0)
        
        glowing_card("Predicted Career Path", role, f"{conf}% Confidence")
        
        tops = data.get('top_predictions', [])
        if len(tops) > 1:
            st.markdown("### Alternative Career Matches")
            df = pd.DataFrame(tops)
            fig = px.bar(df, x="confidence", y="role", orientation='h', color="confidence", text="confidence")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())
'''

p4 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, metric_card

st.set_page_config(page_title="Resume Score", page_icon="📊", layout="wide")
inject_global_css()

try:
    section_title("Resume Score", "📊")
    if 'scoring_data' not in st.session_state or st.session_state['scoring_data'] is None:
        st.warning("Please upload a resume on the Home page first.")
    else:
        data = st.session_state['scoring_data']
        overall = data.get('overall_score', 0)
        st.markdown(f"<h2 style='text-align:center; color:var(--primary); font-size:4rem;'>{overall}/100</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: metric_card("Impact", f"{data.get('impact_score',0)}%", "💥")
        with c2: metric_card("Clarity", f"{data.get('clarity_score',0)}%", "✨")
        with c3: metric_card("Completeness", f"{data.get('completeness_score',0)}%", "📋")
except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())
'''

p5 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, ai_insight_card

st.set_page_config(page_title="Skill Gap Analysis", page_icon="🧩", layout="wide")
inject_global_css()

try:
    section_title("Skill Gap Analysis", "🧩")
    if 'skill_gap_data' not in st.session_state or st.session_state['skill_gap_data'] is None:
        st.warning("Please upload a resume on the Home page first.")
    else:
        data = st.session_state['skill_gap_data']
        ai_insight_card(
            strengths=data.get('present_skills', []),
            weaknesses=data.get('missing_skills', []),
            recommendation=data.get('recommendation', 'Keep learning!')
        )
except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())
'''

p6 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, timeline_step

st.set_page_config(page_title="Learning Roadmap", page_icon="🗺️", layout="wide")
inject_global_css()

try:
    section_title("Learning Roadmap", "🗺️")
    if 'skill_gap_data' not in st.session_state or st.session_state['skill_gap_data'] is None:
        st.warning("Please upload a resume on the Home page first.")
    else:
        data = st.session_state['skill_gap_data']
        steps = data.get('roadmap_steps', [])
        for i, step in enumerate(steps):
            timeline_step(i+1, step.get('title',''), step.get('description',''), is_last=(i==len(steps)-1))
except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())
'''

p7 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
inject_global_css()

try:
    section_title("Executive Dashboard", "📈")
    st.info("Explore detailed metrics in the sidebar pages. All insights are powered by your uploaded resume.")
    if st.button("Reset Session"):
        st.session_state.clear()
        st.switch_page("pages/01_Home.py")
except Exception as e:
    import traceback
    st.error("An unexpected error occurred.")
    with st.expander("Details"): st.code(traceback.format_exc())
'''

p8 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title, premium_card

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")
inject_global_css()
section_title("About AI Career Intelligence", "ℹ️")
premium_card("Our Mission", "To empower tech professionals by providing AI-driven insights into their resumes and career paths.", "🚀")
'''

p9 = '''import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.ui_components import inject_global_css, section_title

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
inject_global_css()
section_title("Settings", "⚙️")
st.write("Application settings and configurations.")
'''

open(os.path.join(pages_dir, '03_Career_Prediction.py'), 'w', encoding='utf-8').write(p3)
open(os.path.join(pages_dir, '04_Resume_Score.py'), 'w', encoding='utf-8').write(p4)
open(os.path.join(pages_dir, '05_Skill_Gap.py'), 'w', encoding='utf-8').write(p5)
open(os.path.join(pages_dir, '06_Learning_Roadmap.py'), 'w', encoding='utf-8').write(p6)
open(os.path.join(pages_dir, '07_Dashboard.py'), 'w', encoding='utf-8').write(p7)
open(os.path.join(pages_dir, '08_About.py'), 'w', encoding='utf-8').write(p8)
open(os.path.join(pages_dir, '09_Settings.py'), 'w', encoding='utf-8').write(p9)
print('Restored pages')

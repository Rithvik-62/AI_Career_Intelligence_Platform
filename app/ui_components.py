import streamlit as st

def inject_global_css():
    css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

/* Hide Default Streamlit Header & Footer Elements */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* Global Typography & Aurora Theme Tokens */
:root {
    --bg-color: #070714;
    --sidebar-color: #0C0C20;
    --primary: #7C3AED;
    --primary-glow: rgba(124, 58, 237, 0.35);
    --secondary: #3B82F6;
    --accent: #06B6D4;
    --accent-glow: rgba(6, 182, 212, 0.35);
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --card-bg: rgba(15, 15, 35, 0.65);
    --card-border: rgba(124, 58, 237, 0.2);
    --card-border-hover: rgba(6, 182, 212, 0.5);
}

.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(124, 58, 237, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.1) 0%, transparent 40%),
                var(--bg-color);
    color: var(--text-main);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em;
    color: var(--text-main) !important;
}

/* Streamlit Sidebar Overrides */
section[data-testid="stSidebar"] {
    background: var(--sidebar-color) !important;
    border-right: 1px solid var(--card-border) !important;
}

/* Sidebar Navigation Items Styling */
div[data-testid="stSidebarNav"] {
    padding-top: 10px;
}
div[data-testid="stSidebarNav"] span {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stSidebarNav"] a {
    border-radius: 12px !important;
    margin: 3px 8px !important;
    padding: 8px 12px !important;
    transition: all 0.25s ease !important;
    border: 1px solid transparent !important;
}
div[data-testid="stSidebarNav"] a:hover {
    background: rgba(124, 58, 237, 0.15) !important;
    border-color: rgba(124, 58, 237, 0.35) !important;
    transform: translateX(3px) !important;
}
div[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.3) 0%, rgba(6,182,212,0.2) 100%) !important;
    border: 1px solid rgba(6,182,212,0.4) !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.25) !important;
}

/* Sidebar Category Headers */
div[data-testid="stSidebarNavSeparator"] {
    border-top: 1px solid rgba(124, 58, 237, 0.2) !important;
    margin: 12px 0 !important;
}

/* Premium Glassmorphism Card */
.premium-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.premium-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.4), transparent);
}
.premium-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 40px rgba(124, 58, 237, 0.25);
    border-color: var(--card-border-hover);
}

/* Glowing Prediction Hero Card */
.glowing-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(6,182,212,0.15) 100%);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 24px;
    padding: 36px;
    box-shadow: 0 0 50px rgba(124,58,237,0.25);
    text-align: center;
    backdrop-filter: blur(20px);
}

/* Status Chips */
.status-chip {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 4px;
    backdrop-filter: blur(8px);
}
.chip-success { background: rgba(16,185,129,0.15); color: var(--success); border: 1px solid rgba(16,185,129,0.3); }
.chip-danger { background: rgba(239,68,68,0.15); color: var(--danger); border: 1px solid rgba(239,68,68,0.3); }
.chip-primary { background: rgba(124,58,237,0.18); color: #A78BFA; border: 1px solid rgba(124,58,237,0.4); }
.chip-accent { background: rgba(6,182,212,0.15); color: var(--accent); border: 1px solid rgba(6,182,212,0.35); }

/* Metric Cards */
.metric-title {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
}
.metric-value {
    font-family: 'Outfit', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #06B6D4 0%, #7C3AED 50%, #F43F5E 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Streamlit Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #7C3AED 0%, #2563EB 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35) !important;
    transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5) !important;
}

/* Timeline */
.timeline-container {
    position: relative;
    padding-left: 40px;
    margin-bottom: 30px;
}
.timeline-node {
    position: absolute;
    left: 0; top: 0;
    width: 24px; height: 24px;
    background: var(--primary);
    border-radius: 50%;
    border: 4px solid var(--bg-color);
    box-shadow: 0 0 15px var(--primary);
    z-index: 2;
}
.timeline-line {
    position: absolute;
    left: 11px; top: 24px; bottom: -30px;
    width: 2px;
    background: linear-gradient(180deg, var(--primary), transparent);
    z-index: 1;
}

/* Section Title */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 14px;
    background: linear-gradient(90deg, #FFFFFF 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Custom Upload Zone */
.upload-zone {
    border: 2px dashed rgba(124, 58, 237, 0.4);
    border-radius: 24px;
    padding: 50px 20px;
    text-align: center;
    background: rgba(124, 58, 237, 0.03);
    transition: all 0.35s ease;
}
.upload-zone:hover {
    background: rgba(124, 58, 237, 0.08);
    border-color: var(--accent);
    box-shadow: 0 0 35px rgba(6, 182, 212, 0.2);
}

/* Pulse animation for chatbot online badge */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.online-indicator {
    display: inline-block;
    width: 10px; height: 10px;
    background-color: #10B981;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    render_sidebar_branding()

def render_sidebar_branding():
    """Renders glowing platform logo header at the top of sidebar."""
    with st.sidebar:
        st.markdown(
            '<div style="text-align:center; padding: 15px 10px 20px 10px; border-bottom: 1px solid rgba(124, 58, 237, 0.25); margin-bottom: 15px;">'
            '<div style="font-size: 2.2rem; margin-bottom: 4px; filter: drop-shadow(0 0 12px rgba(124, 58, 237, 0.6));">🚀</div>'
            '<div style="font-family: \'Outfit\', sans-serif; font-weight: 800; font-size: 1.2rem; background: linear-gradient(135deg, #06B6D4, #7C3AED, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing:0.5px;">CAREER AI PLATFORM</div>'
            '<div style="font-size: 0.76rem; color: #94A3B8; margin-top: 3px; font-weight:500;">v2.0 Data Science & BI Edition</div>'
            '</div>',
            unsafe_allow_html=True
        )

def apply_plotly_theme(fig):
    """Applies global dark theme styling to Plotly figure objects."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Inter, sans-serif"),
        colorway=["#7C3AED", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#EC4899"],
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_xaxes(gridcolor="rgba(124,58,237,0.12)", zerolinecolor="rgba(124,58,237,0.2)")
    fig.update_yaxes(gridcolor="rgba(124,58,237,0.12)", zerolinecolor="rgba(124,58,237,0.2)")
    return fig

def render_aria_sidebar_chatbot():
    """Renders ARIA Assistant in Streamlit sidebar with live indicator and form submit."""
    from utils.chatbot import ARIAChatbot
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<div>'
            '<span class="online-indicator"></span>'
            '<strong style="font-size:1.05rem; color:var(--text-main);">🤖 ARIA AI Assistant</strong>'
            '<span style="float:right; font-size:0.75rem; color:var(--success); background:rgba(16,185,129,0.15); padding:2px 8px; border-radius:10px; border:1px solid rgba(16,185,129,0.3);">Gemini 3.6</span>'
            '</div>',
            unsafe_allow_html=True
        )
        st.caption("Conversational AI tailored to your profile & market trends.")
        
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = [
                {"role": "assistant", "content": "Hi! I'm ARIA, powered by Google Gemini AI. Ask me about alternative career domains, your score, missing skills, or interview prep!"}
            ]
            
        for msg in st.session_state['chat_history'][-4:]:
            st.markdown(f"**{'👤 You' if msg['role']=='user' else '🤖 ARIA'}:** {msg['content']}")
            
        with st.form(key="aria_sidebar_form", clear_on_submit=True):
            user_input = st.text_input("Message ARIA...", placeholder="e.g. How to prepare for Data Science interview?")
            submitted = st.form_submit_button("Send AI Query 💬", use_container_width=True)
            if submitted and user_input.strip():
                st.session_state['chat_history'].append({"role": "user", "content": user_input.strip()})
                reply = ARIAChatbot.get_response(user_input.strip(), st.session_state)
                st.session_state['chat_history'].append({"role": "assistant", "content": reply})
                st.rerun()

def premium_card(title, content, icon=""):
    html = (
        f'<div class="premium-card">'
        f'<div style="display:flex; align-items:center; margin-bottom:16px;">'
        f'<span style="font-size:1.6rem; margin-right:12px; filter:drop-shadow(0 0 8px rgba(124,58,237,0.5));">{icon}</span>'
        f'<h3 style="margin:0; font-weight:700; font-size:1.25rem; background:linear-gradient(90deg, #F8FAFC, #CBD5E1); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{title}</h3>'
        f'</div>'
        f'<div style="color:var(--text-muted); line-height:1.6; font-size:0.95rem;">{content}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_experience_card(exp_dict):
    title = exp_dict.get('job_title', 'Unknown Role')
    company = exp_dict.get('company', 'Unknown Company')
    dates = exp_dict.get('dates', 'Unknown Dates')
    desc = exp_dict.get('description', '')
    desc_html = f"<div style='margin-top:12px; font-size:0.95rem; white-space:pre-wrap;'>{desc}</div>" if desc else ""
    
    content = (
        f'<div style="margin-bottom:4px;">'
        f'<strong style="color:var(--text-main); font-size:1.1rem;">{title}</strong>'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
        f'<span style="color:var(--secondary); font-weight:500;">{company}</span>'
        f'<span style="color:var(--text-muted); font-size:0.85rem; background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:12px;">{dates}</span>'
        f'</div>'
        f'{desc_html}'
    )
    premium_card("Work Experience", content, "🏢")

def render_project_card(proj_dict):
    title = proj_dict.get('project_title', 'Unknown Project')
    techs = proj_dict.get('technologies', [])
    desc = proj_dict.get('description', '')
    desc_html = f"<div style='margin-top:12px; font-size:0.95rem; white-space:pre-wrap;'>{desc}</div>" if desc else ""
    
    techs_html = ""
    if techs:
        techs_html = "<div style='margin-top:10px;'>" + "".join([status_chip(t, "accent") for t in techs]) + "</div>"
        
    content = (
        f'<div style="margin-bottom:8px;">'
        f'<strong style="color:var(--text-main); font-size:1.1rem;">{title}</strong>'
        f'</div>'
        f'{desc_html}'
        f'{techs_html}'
    )
    premium_card("Project", content, "💻")

def render_education_card(edu_dict):
    degree = edu_dict.get('degree', 'Unknown Degree')
    univ = edu_dict.get('university', 'Unknown University')
    desc = edu_dict.get('description', '')
    desc_html = f"<div style='margin-top:8px; font-size:0.95rem; white-space:pre-wrap;'>{desc}</div>" if desc else ""
    
    content = (
        f'<div style="margin-bottom:4px;">'
        f'<strong style="color:var(--text-main); font-size:1.1rem;">{degree}</strong>'
        f'</div>'
        f'<div style="color:var(--secondary); font-weight:500; margin-bottom:8px;">{univ}</div>'
        f'{desc_html}'
    )
    premium_card("Education Record", content, "🏛️")

def ai_insight_card(strengths, weaknesses, recommendation):
    strengths_html = "".join([f'<div style="margin-bottom:8px;">✓ {s}</div>' for s in strengths])
    weaknesses_html = "".join([f'<div style="margin-bottom:8px;">✗ {w}</div>' for w in weaknesses])
    
    html = (
        f'<div class="premium-card" style="border-left: 4px solid var(--accent);">'
        f'<div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">'
        f'<span style="font-size:2rem;">🤖</span>'
        f'<h3 style="margin:0;">AI Career Advisor</h3>'
        f'</div>'
        f'<div style="display:flex; flex-wrap:wrap; gap:20px; margin-bottom:24px;">'
        f'<div style="flex:1; min-width:200px;">'
        f'<h4 style="color:var(--success); margin-bottom:12px;">💪 Strengths Detected</h4>'
        f'{strengths_html}'
        f'</div>'
        f'<div style="flex:1; min-width:200px;">'
        f'<h4 style="color:var(--danger); margin-bottom:12px;">⚠️ Missing Core Skills</h4>'
        f'{weaknesses_html}'
        f'</div>'
        f'</div>'
        f'<div style="background:rgba(255,255,255,0.05); padding:16px; border-radius:12px;">'
        f'<h4 style="color:var(--accent); margin-bottom:8px;">💡 Recommended Next Steps</h4>'
        f'<div style="color:var(--text-muted); line-height:1.6;">{recommendation}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def metric_card(title, value, icon="", subtitle=""):
    html = (
        f'<div class="premium-card" style="text-align:center;">'
        f'<div class="metric-title">{icon} {title}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div style="color:var(--text-muted); font-size:0.85rem; margin-top:8px;">{subtitle}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def glowing_card(title, value, subtitle=""):
    html = (
        f'<div class="glowing-card">'
        f'<h2 style="margin-bottom:8px; color:var(--text-muted); font-size:1.4rem;">{title}</h2>'
        f'<div style="font-size:3.6rem; font-weight:800; color:var(--text-main); margin-bottom:16px; font-family:\'Outfit\', sans-serif;">{value}</div>'
        f'<div class="status-chip chip-primary" style="font-size:1.05rem;">{subtitle}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def status_chip(label, style="primary"):
    return f'<span class="status-chip chip-{style}">{label}</span>'

def render_chips(labels, style="primary"):
    chips = "".join([status_chip(l, style) for l in labels])
    st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)

def timeline_step(number, title, desc, icon="📍", is_last=False):
    line_html = "" if is_last else '<div class="timeline-line"></div>'
    html = (
        f'<div class="timeline-container">'
        f'<div class="timeline-node"></div>'
        f'{line_html}'
        f'<div class="premium-card" style="margin-left: 10px; margin-top: -10px;">'
        f'<div style="font-size:0.85rem; color:var(--accent); font-weight:700; letter-spacing:1px; margin-bottom:8px;">STEP {number}</div>'
        f'<div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">'
        f'<span style="font-size:1.5rem;">{icon}</span>'
        f'<h3 style="margin:0; font-size:1.25rem;">{title}</h3>'
        f'</div>'
        f'<p style="color:var(--text-muted); margin:0; font-size:0.95rem;">{desc}</p>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def section_title(title, icon=""):
    st.markdown(f'<div class="section-title"><span>{icon}</span> {title}</div>', unsafe_allow_html=True)

def hero_banner():
    html = (
        f'<div style="text-align:center; padding: 40px 20px 60px 20px;">'
        f'<div style="display:inline-block; padding: 6px 18px; border-radius:30px; background:rgba(124,58,237,0.15); border:1px solid rgba(124,58,237,0.35); color:#A78BFA; font-weight:600; font-size:0.88rem; margin-bottom:20px;">'
        f'⚡ Powered by Google Gemini 3.6 AI & Scikit-Learn ML'
        f'</div>'
        f'<h1 style="font-size: 4rem; font-weight: 900; margin-bottom: 20px; line-height: 1.15; font-family:\'Outfit\', sans-serif;">'
        f'<span style="background: linear-gradient(135deg, #06B6D4 0%, #7C3AED 50%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">'
        f'AI Career Intelligence Platform'
        f'</span>'
        f'</h1>'
        f'<p style="font-size: 1.35rem; color: #94A3B8; max-width: 760px; margin: 0 auto 30px auto; line-height: 1.6;">'
        f'Transform your resume into a data-driven career roadmap. Predict your optimal trajectory, bridge critical skill gaps, and generate tailored AI assets.'
        f'</p>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

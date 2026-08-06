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

/* Global Typography & Palette Tokens */
:root {
    --bg-color: #0F172A;
    --sidebar-color: #0B1120;
    --card-bg: rgba(17, 24, 39, 0.75);
    --card-border: rgba(37, 99, 235, 0.2);
    --card-border-hover: rgba(6, 182, 212, 0.45);
    --primary: #2563EB;
    --primary-glow: rgba(37, 99, 235, 0.35);
    --secondary: #3B82F6;
    --accent: #06B6D4;
    --accent-glow: rgba(6, 182, 212, 0.35);
    --success: #22C55E;
    --warning: #F59E0B;
    --danger: #EF4444;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
}

/* Micro Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseGlow {
    0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.4); }
    70% { box-shadow: 0 0 0 12px rgba(37, 99, 235, 0); }
    100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.stApp {
    background: radial-gradient(circle at 12% 12%, rgba(37, 99, 235, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 88% 88%, rgba(6, 182, 212, 0.1) 0%, transparent 45%),
                var(--bg-color);
    color: var(--text-main);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    animation: fadeIn 0.4s ease-out;
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
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Sidebar Navigation Items Styling */
div[data-testid="stSidebarNav"] {
    padding-top: 10px;
}
div[data-testid="stSidebarNav"] span {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.94rem !important;
}
div[data-testid="stSidebarNav"] a {
    border-radius: 10px !important;
    margin: 3px 8px !important;
    padding: 8px 12px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid transparent !important;
}
div[data-testid="stSidebarNav"] a:hover {
    background: rgba(37, 99, 235, 0.15) !important;
    border-color: rgba(37, 99, 235, 0.3) !important;
    transform: translateX(4px) !important;
}
div[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(6, 182, 212, 0.18) 100%) !important;
    border: 1px solid rgba(6, 182, 212, 0.35) !important;
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.2) !important;
}

/* Sidebar Category Headers */
div[data-testid="stSidebarNavSeparator"] {
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin: 12px 0 !important;
}

/* Premium Glassmorphism Card */
.premium-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.4s ease-out;
}
.premium-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.4), transparent);
}
.premium-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 32px rgba(37, 99, 235, 0.22);
    border-color: var(--card-border-hover);
}

/* Glowing Hero Card */
.glowing-card {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(6, 182, 212, 0.12) 100%);
    border: 1px solid rgba(37, 99, 235, 0.35);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 0 40px rgba(37, 99, 235, 0.2);
    text-align: center;
    backdrop-filter: blur(20px);
    animation: fadeIn 0.5s ease-out;
}

/* Status Chips */
.status-chip {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 16px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 3px;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
}
.status-chip:hover {
    transform: scale(1.04);
}
.chip-success { background: rgba(34, 197, 94, 0.15); color: var(--success); border: 1px solid rgba(34, 197, 94, 0.3); }
.chip-danger { background: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.3); }
.chip-primary { background: rgba(37, 99, 235, 0.18); color: #93C5FD; border: 1px solid rgba(37, 99, 235, 0.35); }
.chip-accent { background: rgba(6, 182, 212, 0.15); color: var(--accent); border: 1px solid rgba(6, 182, 212, 0.3); }
.chip-warning { background: rgba(245, 158, 11, 0.15); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); }

/* Metric Cards */
.metric-title {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    font-weight: 600;
}
.metric-value {
    font-family: 'Outfit', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #F8FAFC 0%, #06B6D4 50%, #2563EB 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Streamlit Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 0.4px !important;
    box-shadow: 0 4px 18px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.25s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.45) !important;
}

/* Secondary Button */
div.stButton > button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: var(--text-main) !important;
    box-shadow: none !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: rgba(37, 99, 235, 0.2) !important;
    border-color: var(--primary) !important;
}

/* Timeline */
.timeline-container {
    position: relative;
    padding-left: 36px;
    margin-bottom: 24px;
}
.timeline-node {
    position: absolute;
    left: 0; top: 2px;
    width: 20px; height: 20px;
    background: var(--primary);
    border-radius: 50%;
    border: 3px solid var(--bg-color);
    box-shadow: 0 0 12px var(--primary-glow);
    z-index: 2;
}
.timeline-line {
    position: absolute;
    left: 9px; top: 22px; bottom: -24px;
    width: 2px;
    background: linear-gradient(180deg, var(--primary), transparent);
    z-index: 1;
}

/* Section Title */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(90deg, #F8FAFC 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Custom Upload Zone */
.upload-zone {
    border: 2px dashed rgba(37, 99, 235, 0.4);
    border-radius: 20px;
    padding: 45px 20px;
    text-align: center;
    background: rgba(37, 99, 235, 0.04);
    transition: all 0.3s ease;
}
.upload-zone:hover {
    background: rgba(37, 99, 235, 0.09);
    border-color: var(--accent);
    box-shadow: 0 0 30px rgba(6, 182, 212, 0.2);
}

/* Pulse animation for chatbot online badge */
.online-indicator {
    display: inline-block;
    width: 9px; height: 9px;
    background-color: #22C55E;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulseGlow 2s infinite;
}

/* Sidebar Footer Styling */
.sidebar-footer {
    padding: 16px 12px 10px 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin-top: 20px;
    font-size: 0.78rem;
    color: var(--text-muted);
    text-align: center;
}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    render_sidebar_branding()

def render_sidebar_branding():
    """Renders glowing platform logo header at the top of sidebar."""
    with st.sidebar:
        st.markdown(
            '<div style="text-align:center; padding: 16px 10px 18px 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 12px;">'
            '<div style="font-size: 2rem; margin-bottom: 4px; filter: drop-shadow(0 0 10px rgba(37, 99, 235, 0.6));">⚡</div>'
            '<div style="font-family: \'Outfit\', sans-serif; font-weight: 800; font-size: 1.15rem; background: linear-gradient(135deg, #06B6D4, #2563EB); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing:0.5px;">CAREER AI PLATFORM</div>'
            '<div style="font-size: 0.74rem; color: #94A3B8; margin-top: 2px; font-weight:500;">v2.0 Enterprise SaaS Edition</div>'
            '</div>',
            unsafe_allow_html=True
        )

def render_sidebar_footer():
    """Renders professional footer at the bottom of the sidebar."""
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-footer">'
            '🟢 <strong>ML Engine Active</strong> &bull; v2.0.0<br>'
            '<span style="font-size:0.72rem; opacity:0.8;">Powered by Scikit-Learn & Gemini AI</span>'
            '</div>',
            unsafe_allow_html=True
        )

def apply_plotly_theme(fig):
    """Applies global dark theme styling to Plotly figure objects matching prompt palette."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Inter, sans-serif"),
        colorway=["#2563EB", "#06B6D4", "#22C55E", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"],
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.12)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.12)")
    return fig

def render_aria_sidebar_chatbot():
    """Renders ARIA Assistant in Streamlit sidebar with live indicator and form submit."""
    from utils.chatbot import ARIAChatbot
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            '<div>'
            '<span class="online-indicator"></span>'
            '<strong style="font-size:1.02rem; color:var(--text-main);">🤖 ARIA AI Assistant</strong>'
            '<span style="float:right; font-size:0.72rem; color:var(--success); background:rgba(34,197,94,0.15); padding:2px 7px; border-radius:10px; border:1px solid rgba(34,197,94,0.3);">Gemini Active</span>'
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
                
    render_sidebar_footer()

def premium_card(title, content, icon=""):
    html = (
        f'<div class="premium-card">'
        f'<div style="display:flex; align-items:center; margin-bottom:14px;">'
        f'<span style="font-size:1.5rem; margin-right:10px; filter:drop-shadow(0 0 6px rgba(37,99,235,0.4));">{icon}</span>'
        f'<h3 style="margin:0; font-weight:700; font-size:1.2rem; background:linear-gradient(90deg, #F8FAFC, #CBD5E1); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{title}</h3>'
        f'</div>'
        f'<div style="color:var(--text-muted); line-height:1.6; font-size:0.93rem;">{content}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_experience_card(exp_dict):
    title = exp_dict.get('job_title', 'Unknown Role')
    company = exp_dict.get('company', 'Unknown Company')
    dates = exp_dict.get('dates', 'Unknown Dates')
    desc = exp_dict.get('description', '')
    desc_html = f"<div style='margin-top:10px; font-size:0.93rem; white-space:pre-wrap;'>{desc}</div>" if desc else ""
    
    content = (
        f'<div style="margin-bottom:4px;">'
        f'<strong style="color:var(--text-main); font-size:1.05rem;">{title}</strong>'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">'
        f'<span style="color:var(--secondary); font-weight:500;">{company}</span>'
        f'<span style="color:var(--text-muted); font-size:0.82rem; background:rgba(255,255,255,0.08); padding:2px 8px; border-radius:10px;">{dates}</span>'
        f'</div>'
        f'{desc_html}'
    )
    premium_card("Work Experience", content, "🏢")

def render_project_card(proj_dict):
    title = proj_dict.get('project_title', 'Unknown Project')
    techs = proj_dict.get('technologies', [])
    desc = proj_dict.get('description', '')
    desc_html = f"<div style='margin-top:10px; font-size:0.93rem; white-space:pre-wrap;'>{desc}</div>" if desc else ""
    
    techs_html = ""
    if techs:
        techs_html = "<div style='margin-top:8px;'>" + "".join([status_chip(t, "accent") for t in techs]) + "</div>"
        
    content = (
        f'<div style="margin-bottom:6px;">'
        f'<strong style="color:var(--text-main); font-size:1.05rem;">{title}</strong>'
        f'</div>'
        f'{desc_html}'
        f'{techs_html}'
    )
    premium_card("Project", content, "💻")

def render_education_card(edu_dict):
    degree = edu_dict.get('degree', 'Unknown Degree')
    univ = edu_dict.get('university', 'Unknown University')
    desc = edu_dict.get('description', '')
    desc_html = f"<div style='margin-top:8px; font-size:0.93rem; white-space:pre-wrap;'>{desc}</div>" if desc else ""
    
    content = (
        f'<div style="margin-bottom:4px;">'
        f'<strong style="color:var(--text-main); font-size:1.05rem;">{degree}</strong>'
        f'</div>'
        f'<div style="color:var(--secondary); font-weight:500; margin-bottom:6px;">{univ}</div>'
        f'{desc_html}'
    )
    premium_card("Education Record", content, "🏛️")

def ai_insight_card(strengths, weaknesses, recommendation):
    strengths_html = "".join([f'<div style="margin-bottom:6px; color:#A7F3D0;">✓ {s}</div>' for s in strengths])
    weaknesses_html = "".join([f'<div style="margin-bottom:6px; color:#FCA5A5;">✗ {w}</div>' for w in weaknesses])
    
    html = (
        f'<div class="premium-card" style="border-left: 4px solid var(--accent);">'
        f'<div style="display:flex; align-items:center; gap:10px; margin-bottom:18px;">'
        f'<span style="font-size:1.8rem;">🤖</span>'
        f'<h3 style="margin:0; font-size:1.2rem;">AI Executive Insight</h3>'
        f'</div>'
        f'<div style="display:flex; flex-wrap:wrap; gap:16px; margin-bottom:20px;">'
        f'<div style="flex:1; min-width:200px;">'
        f'<h4 style="color:var(--success); margin-bottom:10px; font-size:1rem;">💪 Identified Core Strengths</h4>'
        f'{strengths_html}'
        f'</div>'
        f'<div style="flex:1; min-width:200px;">'
        f'<h4 style="color:var(--danger); margin-bottom:10px; font-size:1rem;">⚠️ Critical Skill Gaps</h4>'
        f'{weaknesses_html}'
        f'</div>'
        f'</div>'
        f'<div style="background:rgba(255,255,255,0.04); padding:14px; border-radius:10px;">'
        f'<h4 style="color:var(--accent); margin-bottom:6px; font-size:0.95rem;">💡 Recommended Career Next Steps</h4>'
        f'<div style="color:var(--text-muted); line-height:1.55; font-size:0.9rem;">{recommendation}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def metric_card(title, value, icon="", subtitle=""):
    html = (
        f'<div class="premium-card" style="text-align:center;">'
        f'<div class="metric-title">{icon} {title}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div style="color:var(--text-muted); font-size:0.82rem; margin-top:6px;">{subtitle}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def glowing_card(title, value, subtitle=""):
    html = (
        f'<div class="glowing-card">'
        f'<h2 style="margin-bottom:6px; color:var(--text-muted); font-size:1.3rem;">{title}</h2>'
        f'<div style="font-size:3.4rem; font-weight:800; color:var(--text-main); margin-bottom:14px; font-family:\'Outfit\', sans-serif;">{value}</div>'
        f'<div class="status-chip chip-primary" style="font-size:1rem;">{subtitle}</div>'
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
        f'<div class="premium-card" style="margin-left: 10px; margin-top: -8px;">'
        f'<div style="font-size:0.8rem; color:var(--accent); font-weight:700; letter-spacing:1px; margin-bottom:6px;">PHASE {number}</div>'
        f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">'
        f'<span style="font-size:1.4rem;">{icon}</span>'
        f'<h3 style="margin:0; font-size:1.15rem;">{title}</h3>'
        f'</div>'
        f'<p style="color:var(--text-muted); margin:0; font-size:0.92rem; line-height:1.5;">{desc}</p>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def section_title(title, icon=""):
    st.markdown(f'<div class="section-title"><span>{icon}</span> {title}</div>', unsafe_allow_html=True)

def hero_banner():
    html = (
        f'<div style="text-align:center; padding: 36px 16px 50px 16px;">'
        f'<div style="display:inline-block; padding: 5px 16px; border-radius:24px; background:rgba(37,99,235,0.12); border:1px solid rgba(37,99,235,0.3); color:#93C5FD; font-weight:600; font-size:0.85rem; margin-bottom:18px;">'
        f'⚡ Enterprise SaaS Edition &bull; Powered by Gemini 3.6 AI & Scikit-Learn'
        f'</div>'
        f'<h1 style="font-size: 3.8rem; font-weight: 900; margin-bottom: 16px; line-height: 1.12; font-family:\'Outfit\', sans-serif;">'
        f'<span style="background: linear-gradient(135deg, #F8FAFC 0%, #06B6D4 50%, #2563EB 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">'
        f'AI Career Intelligence Platform'
        f'</span>'
        f'</h1>'
        f'<p style="font-size: 1.25rem; color: #94A3B8; max-width: 740px; margin: 0 auto 26px auto; line-height: 1.6;">'
        f'Transform your resume into a data-driven career roadmap. Predict your optimal tech trajectory, bridge skill gaps, and generate tailored cover letters.'
        f'</p>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

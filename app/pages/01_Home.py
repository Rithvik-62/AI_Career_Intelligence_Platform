import streamlit as st
import sys, os, tempfile, time, textwrap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.parser import ResumeParser
from utils.predictor import CareerPredictor
from utils.scoring import ResumeScorer
from utils.skill_gap import SkillGapAnalyzer
from utils.insights import InsightEngine
from app.ui_components import inject_global_css, hero_banner, premium_card, render_aria_sidebar_chatbot

st.set_page_config(page_title="AI Career Intelligence Platform", page_icon="🚀", layout="wide")
inject_global_css()
render_aria_sidebar_chatbot()

try:
    # Hero Section
    hero_banner()

    # Feature Cards using Aurora UI Components
    col1, col2, col3 = st.columns(3)
    with col1:
        premium_card("Intelligent Parsing", "Extracts skills and projects natively from PDFs with deep NLP feature extraction.", "📄")
    with col2:
        premium_card("Career Prediction", "Decision Tree & SVM models recommend your ideal tech role with statistical confidence.", "🔮")
    with col3:
        premium_card("Gemini 3.6 AI Power", "Generates custom cover letters, resume rewrites, and 90-day transition roadmaps.", "⚡")

    st.markdown("---")

    # Initialize session state variables
    for k in ['parsed_data', 'prediction_data', 'scoring_data', 'skill_gap_data', 'insights_data', 'match_data']:
        if k not in st.session_state:
            st.session_state[k] = None

    def get_predictor():
        models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
        return CareerPredictor(models_dir=models_dir)

    # Demo Mode Toggle
    st.markdown("---")
    colA, colB = st.columns([3, 1])
    with colA:
        st.markdown("### 🎓 Presentation Demo Mode")
        st.caption("Instantly populate the application with Gold Standard profiles for recruiter & classroom presentations.")
        demo_profiles = {
            "Data Scientist": {
                'parsed': {
                    'name': 'Alex Rivera', 'email': 'alex.rivera@example.com', 'phone': '+1 (555) 234-5678',
                    'location': 'San Francisco, CA', 'linkedin': 'https://linkedin.com/in/alexrivera', 'github': 'https://github.com/alexrivera', 'portfolio': 'https://alexrivera.dev',
                    'skills': ['Python', 'Machine Learning', 'TensorFlow', 'SQL', 'Data Visualization', 'Pandas', 'Keras', 'Scikit-Learn'],
                    'experience': [{'job_title': 'Senior Data Scientist', 'company': 'TechNova AI', 'dates': '2021-Present', 'description': 'Built customer churn models.'}],
                    'education': [{'degree': 'M.S. Computer Science', 'university': 'State University', 'description': 'Specialized in Artificial Intelligence.'}],
                    'projects': [{'project_title': 'Predictive Analytics Engine', 'technologies': ['Python', 'TensorFlow'], 'description': 'Built a customer churn model using XGBoost.'}],
                    'certifications': [{'title': 'TensorFlow Developer Certificate', 'description': 'Deep Learning & ML Model Deployment'}]
                },
                'prediction': {
                    'predicted_role': 'Data Scientist', 'confidence': 94.5,
                    'top_predictions': [
                        {'rank': 1, 'role': 'Data Scientist', 'confidence': 94.5},
                        {'rank': 2, 'role': 'Machine Learning Engineer', 'confidence': 88.2},
                        {'rank': 3, 'role': 'Data Analyst', 'confidence': 76.4},
                        {'rank': 4, 'role': 'Software Developer', 'confidence': 62.1},
                        {'rank': 5, 'role': 'AI Engineer', 'confidence': 58.0}
                    ],
                    'feature_contributions': [{'feature': 'python', 'weight': 0.42, 'impact': 'High'}, {'feature': 'machine learning', 'weight': 0.38, 'impact': 'High'}, {'feature': 'sql', 'weight': 0.25, 'impact': 'High'}],
                    'explanation': 'Model predicts Data Scientist based on high TF-IDF feature weights for Python, ML, and SQL.'
                },
                'scoring': {
                    'overall_score': 88, 'ats_score': 90, 'completeness_pct': 92.5, 'career_readiness': 89.0, 'strength_index': 86.5,
                    'rating': 'Enterprise Leader (Tier 1)',
                    'category_scores': {'skills': 28, 'experience': 18, 'education': 12, 'projects': 18, 'certifications': 12},
                    'interpretations': {'overall': 'Top tier candidate profile.', 'ats': 'High ATS readability.'},
                    'suggestions': ['Include link to active GitHub repository.']
                },
                'skill_gap': {
                    'target_role': 'Data Scientist', 'acquired_skills': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'TensorFlow'],
                    'missing_skills': ['PyTorch', 'AWS', 'Docker'], 'coverage_pct': 82.5, 'skill_density': 0.85, 'tech_readiness': 88.0,
                    'priority_skills': [{'skill': 'PyTorch', 'priority_rank': 1, 'importance': 'Critical', 'estimated_hours': 20}]
                }
            }
        }
        
        selected_profile = st.selectbox("Select Demo Profile:", list(demo_profiles.keys()), label_visibility="collapsed")
        
    with colB:
        if st.button("🚀 Enable Demo Mode", type="secondary", use_container_width=True):
            profile = demo_profiles[selected_profile]
            st.session_state['parsed_data'] = profile['parsed']
            st.session_state['prediction_data'] = profile['prediction']
            st.session_state['scoring_data'] = profile['scoring']
            st.session_state['skill_gap_data'] = profile['skill_gap']
            st.session_state['insights_data'] = InsightEngine.generate_executive_insights(
                profile['parsed'], profile['scoring'], profile['prediction'], profile['skill_gap']
            )
            st.success(f"✅ Loaded {selected_profile}! Navigate sidebar.")

    st.markdown("---")

    html_upload = textwrap.dedent("""
    <div style="text-align:center; margin-bottom: 24px;">
        <h2 style="font-size:2.2rem; font-weight:800;">Upload Candidate Resume</h2>
        <p style="color:var(--text-muted); font-size:1.05rem;">Drop your PDF resume here to launch full ML classification & Gemini AI evaluation</p>
    </div>
    """)
    st.markdown(html_upload, unsafe_allow_html=True)

    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Resume", type="pdf", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        if st.button("⚡ Initialize AI Analysis Sequence", type="primary", use_container_width=True):
            start_time = time.time()
            loading_placeholder = st.empty()
            
            # Reset old session state variables to guarantee fresh parsing
            for key in ['parsed_data', 'prediction_data', 'scoring_data', 'skill_gap_data', 'insights_data', 'match_data']:
                st.session_state[key] = None
        
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                def update_loading(step_msg, progress_bar):
                    html = (
                        f'<div class="premium-card" style="text-align:center; border:1px solid var(--accent);">'
                        f'<h3 style="color:var(--accent); font-family:\'Outfit\', sans-serif;">🤖 Gemini AI & ML Processing Sequence</h3>'
                        f'<div style="color:var(--primary); font-size:1.5rem; letter-spacing:5px;">{progress_bar}</div>'
                        f'<p style="color:var(--text-muted); font-weight:500; margin-top:10px;">{step_msg}</p>'
                        f'</div>'
                    )
                    loading_placeholder.markdown(html, unsafe_allow_html=True)
            
                update_loading("Uploading Resume PDF...", "█░░░░░░░░░")
                time.sleep(0.2)
            
                update_loading("Parsing Resume Text & Entities...", "███░░░░░░░")
                parser = ResumeParser()
                parsed_data = parser.parse(tmp_path)
            
                if "error" in parsed_data:
                    st.error(f"Parser Error: {parsed_data['error']}")
                else:
                    st.session_state['parsed_data'] = parsed_data
                
                    update_loading("Predicting Career Trajectory (Top 5)...", "██████░░░░")
                    predictor = get_predictor()
                    prediction_data = predictor.predict(tmp_path)
                
                    if "error" in prediction_data:
                        st.error(f"Prediction Error: {prediction_data['error']}")
                    else:
                        st.session_state['prediction_data'] = prediction_data
                    
                        update_loading("Calculating Multi-Dimensional Metrics...", "████████░░")
                        scorer = ResumeScorer()
                        scoring_data = scorer.score_resume(parsed_data)
                        st.session_state['scoring_data'] = scoring_data
                    
                        update_loading("Executing Skill Gap & Priority Ranking...", "█████████░")
                        analyzer = SkillGapAnalyzer()
                        skill_gap_data = analyzer.analyze(parsed_data, prediction_data['predicted_role'])
                        st.session_state['skill_gap_data'] = skill_gap_data
                        
                        update_loading("Generating AI Insights & PDF Assets...", "██████████")
                        insights_data = InsightEngine.generate_executive_insights(
                            parsed_data, scoring_data, prediction_data, skill_gap_data
                        )
                        st.session_state['insights_data'] = insights_data
                        time.sleep(0.2)
                    
                        exec_time = round(time.time() - start_time, 2)
                        loading_placeholder.empty()
                        
                        st.markdown(
                            f'<div class="premium-card" style="border-left: 4px solid var(--success);">'
                            f'<h3 style="color:var(--success); margin:0;">✅ Analysis Complete in {exec_time}s!</h3>'
                            f'<p style="margin-top:10px;">Your intelligent career analytics are ready. Navigate the sidebar to explore.</p>'
                            f'</div>', 
                            unsafe_allow_html=True
                        )
                    
                os.remove(tmp_path)
            
            except Exception as e:
                loading_placeholder.empty()
                st.error(f"An unexpected error occurred while processing your resume: {str(e)}")

    elif st.session_state.get('parsed_data') is not None:
        st.markdown(
            '<div class="premium-card" style="border-left: 4px solid var(--primary); text-align:center;">'
            '<h3 style="color:var(--primary); margin:0;">🎉 Candidate Profile Active</h3>'
            '<p style="margin-top:10px;">Your data is loaded. Use the sidebar to access AI Cover Letter Generator, Career Switch Advisor, and Executive Dashboards.</p>'
            '</div>', 
            unsafe_allow_html=True
        )

except Exception as e:
    import traceback
    st.error('An unexpected error occurred while loading this page.')
    with st.expander('View Technical Details'):
        st.code(traceback.format_exc())

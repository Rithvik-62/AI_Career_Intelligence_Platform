"""
ARIA Chatbot Engine (AI Resume Intelligence Assistant)
Powered by Google Gemini AI with offline fallback.
"""

from typing import Dict, Any, List
from utils.gemini_service import GeminiService

class ARIAChatbot:
    """
    Conversational agent providing real-time generative AI Q&A on candidate resumes.
    """
    
    @staticmethod
    def get_response(user_query: str, session_data: Dict[str, Any]) -> str:
        query = user_query.strip()
        
        parsed = session_data.get('parsed_data')
        pred = session_data.get('prediction_data')
        scoring = session_data.get('scoring_data')
        gap = session_data.get('skill_gap_data')
        insights = session_data.get('insights_data')
        
        if not parsed or not pred:
            return "Please upload a resume on the Home page first or click 'Enable Demo Mode' so I can analyze your candidate profile!"
            
        role = pred.get('predicted_role', 'Software Developer')
        conf = pred.get('confidence', 0.0)
        top_preds = pred.get('top_predictions', [])
        overall_score = scoring.get('overall_score', 0) if scoring else 0
        ats_score = scoring.get('ats_score', 0) if scoring else 0
        missing = gap.get('missing_skills', []) if gap else []
        acquired = gap.get('acquired_skills', []) if gap else []
        
        # 1. Attempt Google Gemini AI Generation
        if GeminiService.is_available():
            system_prompt = (
                f"You are ARIA (AI Resume Intelligence Assistant), an expert technical recruiter and career advisor. "
                f"The candidate's profile summary: "
                f"Name: {parsed.get('name', 'Candidate')}, "
                f"Predicted Career: {role} ({conf}% match), "
                f"Alternative Career Matches: {[p.get('role') for p in top_preds[:3]]}, "
                f"Resume Score: {overall_score}/100, "
                f"ATS Score: {ats_score}%, "
                f"Acquired Skills: {acquired[:6]}, "
                f"Missing Skills: {missing[:5]}. "
                f"Answer the user's question concisely, helpfully, and professionally in markdown."
            )
            ai_reply = GeminiService.generate_response(query, system_prompt)
            if ai_reply:
                return ai_reply

        # 2. Offline Rule-Based Fallback
        q_lower = query.lower()
        
        if any(w in q_lower for w in ['other', 'domain', 'domin', 'field', 'track', 'option', 'alternative', 'try', 'else', 'switch', 'branch']):
            if len(top_preds) > 1:
                alt_list = "\n".join([f"• **{p.get('role', 'N/A')}** ({p.get('confidence', 0)}% Match)" for p in top_preds[1:5]])
                return (
                    f"Based on your resume skills, besides **{role}**, here are other top domains you can pursue:\n\n"
                    f"{alt_list}\n\n"
                    f"💡 *Tip: To switch to these domains, check out the Skill Gap page to see missing skills for each role!*"
                )
            else:
                return f"Your top primary domain is **{role}** ({conf}% match). You can also explore Data Analyst, ML Engineer, or Software Developer tracks!"

        elif any(w in q_lower for w in ['predict', 'career', 'role', 'why', 'chosen', 'job', 'path', 'position', 'recommend']):
            alts = ", ".join([f"{p['role']} ({p['confidence']}%)" for p in top_preds[1:3]]) if len(top_preds) > 1 else "None"
            return (
                f"Based on TF-IDF feature extraction, your primary career trajectory is predicted as **{role}** "
                f"with **{conf}% statistical confidence**.\n\n"
                f"• **Alternative Matches:** {alts}\n"
                f"• **Key Skills Driving Prediction:** {', '.join(acquired[:4]) if acquired else 'Technical Skills'}"
            )
            
        elif any(w in q_lower for w in ['score', 'ats', 'rating', 'grade', 'percentage', 'point', 'metric', 'completeness', 'readiness']):
            return (
                f"Your **Overall Resume Score is {overall_score}/100** ({scoring.get('rating', 'N/A')}).\n\n"
                f"• **ATS Compatibility:** {ats_score}%\n"
                f"• **Resume Completeness:** {scoring.get('completeness_pct', 0)}%\n"
                f"• **Career Readiness:** {scoring.get('career_readiness', 0)}%\n\n"
                f"Your strongest section is **{insights.get('top_strength', 'Skills') if insights else 'Skills'}**."
            )
            
        elif any(w in q_lower for w in ['missing', 'gap', 'lack', 'need', 'learn', 'skill', 'course', 'study', 'roadmap']):
            if missing:
                return (
                    f"For the **{role}** track, you are currently missing **{len(missing)} core skills**:\n\n"
                    f"⚠️ **Key Skill Gaps:** {', '.join(missing[:5])}\n\n"
                    f"💡 **Top Recommendation:** Focus on learning **{missing[0]}** first to maximize your readiness index!"
                )
            else:
                return f"Incredible job! You have acquired 100% of the core competencies required for **{role}**!"
                
        elif any(w in q_lower for w in ['weak', 'improve', 'fix', 'better', 'suggest', 'recommendation', 'rewrite']):
            suggs = scoring.get('suggestions', []) if scoring else []
            sugg_str = "\n".join([f"• {s}" for s in suggs[:3]]) if suggs else "Your profile is well optimized!"
            return f"Here are top priority action items to improve your profile:\n\n{sugg_str}"
            
        elif any(w in q_lower for w in ['hello', 'hi', 'hey', 'who', 'help', 'start']):
            return f"Hello! I am ARIA, your AI Career Intelligence Assistant. You can ask me about alternative domains you can try, your predicted career, resume score, ATS compatibility, or missing skills!"
            
        else:
            alts_brief = ", ".join([p['role'] for p in top_preds[1:3]]) if len(top_preds) > 1 else "other tech roles"
            return (
                f"I analyzed your candidate profile for **{role}** (Score: {overall_score}/100).\n\n"
                f"Here are questions you can ask me:\n"
                f"1. *'Which other domain can I try on?'* (Explores {alts_brief})\n"
                f"2. *'Why was I predicted {role}?'*\n"
                f"3. *'What is my ATS score?'*\n"
                f"4. *'Which skills am I missing?'*"
            )

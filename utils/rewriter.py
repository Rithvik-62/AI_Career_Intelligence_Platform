"""
Resume Rewriter Suggestion Engine
Generates quantifiable, action-verb driven Before/After improvements using Google Gemini AI with offline fallback.
"""

from typing import Dict, Any, List
from utils.gemini_service import GeminiService

class ResumeRewriter:
    """
    Prescriptive NLP tool converting passive bullet points into high-impact enterprise resume achievements.
    """
    
    PATTERNS = [
        {
            "category": "Machine Learning & AI",
            "before": "Worked on a machine learning project using Python.",
            "after": "Architected an end-to-end Machine Learning pipeline using Python (Scikit-Learn, Pandas) achieving 94.2% classification accuracy across 10,000+ data points.",
            "impact": "+35% Recruiter Response Rate"
        },
        {
            "category": "Software Engineering & Web",
            "before": "Built a web app with React and Node.js.",
            "after": "Engineered a scalable full-stack web application using React and Node.js REST APIs, decreasing average latency by 40% for over 500 active users.",
            "impact": "+28% Technical Rating"
        },
        {
            "category": "Data Analytics & SQL",
            "before": "Created SQL queries and Excel dashboards.",
            "after": "Designed complex SQL queries and automated Power BI dashboards, saving 12 hours weekly in operational reporting for cross-functional stakeholders.",
            "impact": "+30% Analytics Score"
        },
        {
            "category": "Cloud & DevOps",
            "before": "Deployed application on AWS cloud.",
            "after": "Orchestrated containerized microservices deployment on AWS using Docker and Kubernetes, maintaining 99.9% uptime SLA.",
            "impact": "+40% DevOps Alignment"
        }
    ]
    
    @classmethod
    def get_rewriter_suggestions(cls, parsed_data: Dict[str, Any], target_role: str) -> List[Dict[str, str]]:
        skills = [s.lower() for s in parsed_data.get('skills', [])]
        suggestions = []
        
        # 1. Try Gemini AI dynamic generation if active
        if GeminiService.is_available() and skills:
            try:
                sample_bullet = f"Worked with {skills[0]} to build applications."
                ai_suggestion = GeminiService.rewrite_resume_bullet(sample_bullet, target_role)
                if ai_suggestion and isinstance(ai_suggestion, dict) and "after" in ai_suggestion:
                    suggestions.append({
                        "category": ai_suggestion.get("category", target_role),
                        "before": ai_suggestion.get("before", sample_bullet),
                        "after": ai_suggestion.get("after", ""),
                        "impact": ai_suggestion.get("impact", "+35% Recruiter Impact")
                    })
            except Exception:
                pass
                
        # 2. Rule-based fallback suggestions
        if any(s in skills for s in ['python', 'machine learning', 'tensorflow', 'scikit-learn']):
            suggestions.append(cls.PATTERNS[0])
            
        if any(s in skills for s in ['java', 'javascript', 'react', 'node.js', 'spring boot']):
            suggestions.append(cls.PATTERNS[1])
            
        if any(s in skills for s in ['sql', 'excel', 'power bi', 'tableau']):
            suggestions.append(cls.PATTERNS[2])
            
        if any(s in skills for s in ['aws', 'docker', 'kubernetes', 'devops']):
            suggestions.append(cls.PATTERNS[3])
            
        if not suggestions:
            suggestions = cls.PATTERNS[:2]
            
        return suggestions

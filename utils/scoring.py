"""
Resume Scoring Engine (V2.0 Enhanced)
Evaluates parsed resume data across 9+ granular dimensions, calculating scores,
completeness percentages, career readiness indices, and concise analytical interpretations.
"""

import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResumeScorer:
    """
    Advanced Data Science scoring module computing multi-dimensional analytics
    for candidate resume evaluation.
    """
    
    def __init__(self):
        self.max_scores = {
            "skills": 30,
            "education": 15,
            "projects": 20,
            "experience": 20,
            "certifications": 15
        }

    def _score_skills(self, skills: List[str]) -> tuple[int, str, List[str]]:
        num_skills = len(skills)
        if num_skills >= 12:
            score = 30
            feedback = f"Exceptional technical vocabulary with {num_skills} verified skills detected."
            suggestions = []
        elif num_skills >= 7:
            score = 22
            feedback = f"Good technical skill coverage ({num_skills} skills detected)."
            suggestions = ["Incorporate domain-specific frameworks to strengthen your skill rating."]
        elif num_skills >= 3:
            score = 14
            feedback = f"Basic technical skills ({num_skills} detected)."
            suggestions = ["Significantly expand your technical skill section with core tools."]
        else:
            score = 5
            feedback = "Very few or no technical skills detected."
            suggestions = ["Add a dedicated Technical Skills section with relevant keywords."]
            
        return score, feedback, suggestions

    def _score_education(self, education: List[Any]) -> tuple[int, str, List[str]]:
        if len(education) >= 2:
            score = 15
            feedback = "Strong academic progression with multiple credentials."
            suggestions = []
        elif len(education) == 1:
            score = 10
            feedback = "Foundational academic degree detected."
            suggestions = ["Add specific coursework, GPA, or academic honors if applicable."]
        else:
            score = 0
            feedback = "No formal education history detected."
            suggestions = ["Include degree, institution, and graduation timeline."]
            
        return score, feedback, suggestions

    def _score_projects(self, projects: List[Any]) -> tuple[int, str, List[str]]:
        num_proj = len(projects)
        if num_proj >= 3:
            score = 20
            feedback = "Robust project portfolio demonstrating practical execution."
            suggestions = []
        elif num_proj >= 1:
            score = 12
            feedback = f"Moderate project showcase ({num_proj} project detected)."
            suggestions = ["Add 1-2 additional technical projects with quantifiable impact."]
        else:
            score = 0
            feedback = "No technical projects detected."
            suggestions = ["Include hands-on technical or open-source projects."]
            
        return score, feedback, suggestions

    def _score_experience(self, experience: List[Any]) -> tuple[int, str, List[str]]:
        num_exp = len(experience)
        if num_exp >= 2:
            score = 20
            feedback = "Solid professional background with proven employment history."
            suggestions = []
        elif num_exp == 1:
            score = 12
            feedback = "Initial industry experience detected."
            suggestions = ["Include measurable outcomes (e.g., % improvement) in experience bullets."]
        else:
            score = 5
            feedback = "No explicit work experience section detected."
            suggestions = ["Add internships, freelance work, or open-source contributions."]
            
        return score, feedback, suggestions

    def _score_certifications(self, certifications: List[Any]) -> tuple[int, str, List[str]]:
        num_certs = len(certifications)
        if num_certs >= 2:
            score = 15
            feedback = "Strong continuous learning commitment via multiple industry certifications."
            suggestions = []
        elif num_certs == 1:
            score = 9
            feedback = "Single technical certification verified."
            suggestions = ["Pursue vendor-certified credentials (e.g., AWS, TensorFlow, Azure)."]
        else:
            score = 0
            feedback = "No professional certifications detected."
            suggestions = ["Complete and list relevant technical certifications."]
            
        return score, feedback, suggestions

    def _calculate_ats_score(self, parsed_data: Dict[str, Any]) -> int:
        """Calculates ATS Formatting & Structural Compatibility Score (0-100)."""
        score = 40  # Baseline for valid PDF parsing
        
        if parsed_data.get('email'): score += 10
        if parsed_data.get('phone'): score += 10
        if parsed_data.get('linkedin') or parsed_data.get('github'): score += 10
        if len(parsed_data.get('skills', [])) >= 5: score += 10
        if len(parsed_data.get('education', [])) >= 1: score += 10
        if len(parsed_data.get('experience', [])) >= 1 or len(parsed_data.get('projects', [])) >= 1: score += 10
        
        return min(100, score)

    def _calculate_completeness(self, parsed_data: Dict[str, Any]) -> float:
        """Calculates Resume Completeness % across 8 key structural elements."""
        fields = [
            bool(parsed_data.get('name')),
            bool(parsed_data.get('email')),
            bool(parsed_data.get('phone')),
            bool(parsed_data.get('skills')),
            bool(parsed_data.get('education')),
            bool(parsed_data.get('experience')),
            bool(parsed_data.get('projects')),
            bool(parsed_data.get('certifications') or parsed_data.get('achievements'))
        ]
        return round((sum(fields) / len(fields)) * 100, 1)

    def _get_rating(self, total_score: int) -> str:
        if total_score >= 88: return "Enterprise Leader (Tier 1)"
        if total_score >= 75: return "Highly Competitive"
        if total_score >= 62: return "Job Ready"
        if total_score >= 48: return "Developing Profile"
        return "Requires Optimization"

    def score_resume(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes 9+ analytical metrics and structured feedback.
        """
        logging.info("Starting advanced resume scoring pipeline...")
        
        if "error" in parsed_data:
            return {"error": "Cannot score a resume with parsing errors."}
            
        skills_score, skills_fb, skills_sug = self._score_skills(parsed_data.get('skills', []))
        edu_score, edu_fb, edu_sug = self._score_education(parsed_data.get('education', []))
        proj_score, proj_fb, proj_sug = self._score_projects(parsed_data.get('projects', []))
        exp_score, exp_fb, exp_sug = self._score_experience(parsed_data.get('experience', []))
        cert_score, cert_fb, cert_sug = self._score_certifications(parsed_data.get('certifications', []))
        
        overall_score = skills_score + edu_score + proj_score + exp_score + cert_score
        ats_score = self._calculate_ats_score(parsed_data)
        completeness_pct = self._calculate_completeness(parsed_data)
        
        # Derived Index Calculations
        career_readiness = round((overall_score * 0.6) + (ats_score * 0.4), 1)
        strength_index = round((skills_score / 30 * 40) + (proj_score / 20 * 30) + (exp_score / 20 * 30), 1)

        # Interpretations
        interpretations = {
            "overall": f"Overall score of {overall_score}/100 indicates a '{self._get_rating(overall_score)}' profile.",
            "ats": f"ATS score of {ats_score}% confirms {'high' if ats_score >= 75 else 'moderate'} structural readability for automated screeners.",
            "skills": f"Technical skill score is {skills_score}/30. " + ("Strong alignment with tech stacks." if skills_score >= 20 else "Additional skills recommended."),
            "experience": f"Experience score is {exp_score}/20. " + ("Demonstrates strong career history." if exp_score >= 15 else "Focus on highlighting project outcomes."),
            "education": f"Education score is {edu_score}/15. Credentials are well documented.",
            "projects": f"Project score is {proj_score}/20. " + ("Solid practical evidence." if proj_score >= 12 else "Add practical portfolio items."),
            "certifications": f"Certification score is {cert_score}/15. Continuous learning metric.",
            "completeness": f"Resume completeness is at {completeness_pct}%. " + ("All core sections present." if completeness_pct >= 80 else "Some essential sections are missing."),
            "readiness": f"Career readiness index of {career_readiness}% combines content quality and ATS compliance."
        }

        all_suggestions = skills_sug + edu_sug + proj_sug + exp_sug + cert_sug
        if not parsed_data.get('linkedin'): all_suggestions.append("Add LinkedIn profile link for social verification.")
        if not parsed_data.get('github'): all_suggestions.append("Add GitHub profile link to showcase code repositories.")

        return {
            "overall_score": overall_score,
            "ats_score": ats_score,
            "completeness_pct": completeness_pct,
            "career_readiness": career_readiness,
            "strength_index": strength_index,
            "rating": self._get_rating(overall_score),
            "category_scores": {
                "skills": skills_score,
                "education": edu_score,
                "projects": proj_score,
                "experience": exp_score,
                "certifications": cert_score
            },
            "category_percentages": {
                "skills": round(skills_score / 30 * 100, 1),
                "education": round(edu_score / 15 * 100, 1),
                "projects": round(proj_score / 20 * 100, 1),
                "experience": round(exp_score / 20 * 100, 1),
                "certifications": round(cert_score / 15 * 100, 1)
            },
            "feedback": {
                "skills": skills_fb,
                "education": edu_fb,
                "projects": proj_fb,
                "experience": exp_fb,
                "certifications": cert_fb
            },
            "interpretations": interpretations,
            "suggestions": all_suggestions
        }

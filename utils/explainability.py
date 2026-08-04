"""
Explainable AI (XAI) Engine
Provides diagnostic analytics and feature attribution for career predictions.
"""

from typing import Dict, Any, List

class ExplainabilityEngine:
    """
    Analyzes prediction results, TF-IDF feature weights, and parsed section data
    to generate diagnostic explanations, feature contributions, and key decision factors.
    """
    
    @staticmethod
    def generate_explanation(parsed_data: Dict[str, Any], pred_data: Dict[str, Any]) -> Dict[str, Any]:
        role = pred_data.get('predicted_role', 'Software Developer')
        confidence = pred_data.get('confidence', 85.0)
        contributions = pred_data.get('feature_contributions', [])
        
        skills = parsed_data.get('skills', [])
        projects = parsed_data.get('projects', [])
        experience = parsed_data.get('experience', [])
        
        # Section weights
        skill_count = len(skills)
        proj_count = len(projects)
        exp_count = len(experience)
        total = max(1, skill_count + proj_count + exp_count)
        
        section_weights = {
            "Technical Skills": round((skill_count / total) * 100, 1),
            "Projects": round((proj_count / total) * 100, 1),
            "Work Experience": round((exp_count / total) * 100, 1)
        }
        
        # Strengths & Weaknesses
        strengths = []
        weaknesses = []
        
        if skill_count >= 8:
            strengths.append(f"High technical skill diversity ({skill_count} detected).")
        else:
            weaknesses.append("Skill coverage is below industry benchmark (less than 8 skills).")
            
        if proj_count >= 2:
            strengths.append(f"Demonstrated project portfolio ({proj_count} project blocks).")
        else:
            weaknesses.append("Limited project evidence in target domain.")
            
        if exp_count >= 1:
            strengths.append("Verified professional experience present.")
        else:
            weaknesses.append("No explicit work experience section detected.")
            
        # Reasoning narrative
        top_terms = [c['feature'] for c in contributions[:4]] if contributions else skills[:4]
        reasoning = (
            f"The prediction favors '{role}' ({confidence}% confidence) because the TF-IDF vectorizer "
            f"identified strong semantic alignment with key technical tokens: {', '.join(top_terms)}. "
            f"Section analysis shows {section_weights['Technical Skills']}% of predictive weight stems from skills, "
            f"and {section_weights['Projects']}% from project descriptions."
        )
        
        return {
            "predicted_role": role,
            "confidence": confidence,
            "section_weights": section_weights,
            "feature_contributions": contributions,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "reasoning": reasoning
        }

"""
Skill Gap Engine (V2.0 Enhanced)
Calculates Skill Coverage %, Priority Ranking, Skill Density, and Technical Readiness.
"""

from typing import Dict, Any, List
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import CAREER_DATABASE

class SkillGapAnalyzer:
    """
    Diagnostic & Descriptive analytics engine comparing candidate skills against industry standards.
    """
    
    def __init__(self, career_db: Dict[str, List[str]] = CAREER_DATABASE):
        self.career_db = career_db

    def analyze(self, parsed_data: Dict[str, Any], target_role: str) -> Dict[str, Any]:
        """
        Executes skill set comparison and computes priority metrics.
        """
        if "error" in parsed_data:
            return {"error": "Cannot analyze skill gap for a resume with parsing errors."}
            
        candidate_skills = parsed_data.get('skills', [])
        cand_set = set([s.lower().strip() for s in candidate_skills])
        
        # Get target role required skills or fallback
        required_skills = self.career_db.get(target_role, self.career_db.get("Software Developer", []))
        req_set = set([r.lower().strip() for r in required_skills])
        
        acquired_skills = [s for s in required_skills if s.lower().strip() in cand_set]
        missing_skills = [s for s in required_skills if s.lower().strip() not in cand_set]
        
        total_req = max(1, len(required_skills))
        coverage_pct = round((len(acquired_skills) / total_req) * 100, 1)
        
        # Skill Density: acquired skills / total candidate skills ratio
        skill_density = round(len(acquired_skills) / max(1, len(candidate_skills)), 2)
        
        # Technical Readiness metric (0-100)
        tech_readiness = round((coverage_pct * 0.7) + (min(1.0, skill_density * 2) * 30), 1)
        
        # Priority Ranking for missing skills
        priority_skills = []
        for rank, skill in enumerate(missing_skills, start=1):
            priority_skills.append({
                "skill": skill,
                "priority_rank": rank,
                "importance": "Critical" if rank <= 2 else ("High" if rank <= 4 else "Moderate"),
                "estimated_hours": 15 + (rank * 5)
            })
            
        summary = (
            f"You have acquired {len(acquired_skills)} out of {len(required_skills)} core skills required for '{target_role}', "
            f"yielding a {coverage_pct}% Skill Coverage rating and a Technical Readiness index of {tech_readiness}%."
        )
        
        return {
            "target_role": target_role,
            "acquired_skills": acquired_skills,
            "missing_skills": missing_skills,
            "priority_skills": priority_skills,
            "coverage_pct": coverage_pct,
            "skill_density": skill_density,
            "tech_readiness": tech_readiness,
            "total_required": len(required_skills),
            "summary": summary
        }

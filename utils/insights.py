"""
AI Insight Engine
Automatically extracts key executive insights from resume analytics, scores, and predictions.
"""

from typing import Dict, Any, List

class InsightEngine:
    """
    Synthesizes analytics from Parser, Predictor, Scorer, and SkillGap to produce
    executive decision cards and actionable summaries.
    """
    
    @staticmethod
    def generate_executive_insights(parsed_data: Dict[str, Any], 
                                     score_data: Dict[str, Any], 
                                     pred_data: Dict[str, Any], 
                                     gap_data: Dict[str, Any]) -> Dict[str, Any]:
        
        # 1. Top Strength
        cat_scores = score_data.get('category_scores', {})
        top_cat = max(cat_scores.items(), key=lambda x: x[1])[0] if cat_scores else "skills"
        top_strength = f"Strongest resume category is '{top_cat.title()}' with a score of {cat_scores.get(top_cat, 0)}."
        
        # 2. Weakest Section
        weak_cat = min(cat_scores.items(), key=lambda x: x[1])[0] if cat_scores else "certifications"
        weakest_section = f"Primary area for improvement is '{weak_cat.title()}' (scored {cat_scores.get(weak_cat, 0)})."
        
        # 3. Critical Missing Skill
        missing_skills = gap_data.get('missing_skills', [])
        critical_missing_skill = missing_skills[0] if missing_skills else "None! All core role skills acquired."
        
        # 4. Most Valuable Skill
        acquired = gap_data.get('acquired_skills', [])
        most_valuable = acquired[0] if acquired else (parsed_data.get('skills', ['Python'])[0] if parsed_data.get('skills') else 'Python')
        
        # 5. Highest Impact Recommendation
        highest_impact = f"Master '{critical_missing_skill}' and build a targeted portfolio project for {gap_data.get('target_role', 'your target role')}."
        
        # 6. Readiness Summary
        readiness = score_data.get('career_readiness', 70.0)
        readiness_summary = (
            f"Candidate displays a {readiness}% Career Readiness rating for '{pred_data.get('predicted_role', 'Software Developer')}' "
            f"with an ATS compatibility of {score_data.get('ats_score', 80)}%."
        )
        
        # 7. Priority Matrix
        priority = "High - Focus on Skill Gaps" if gap_data.get('coverage_pct', 100) < 60 else "Moderate - Enhance Portfolio"

        return {
            "top_strength": top_strength,
            "weakest_section": weakest_section,
            "critical_missing_skill": critical_missing_skill,
            "most_valuable_skill": most_valuable,
            "highest_impact_recommendation": highest_impact,
            "career_readiness_summary": readiness_summary,
            "improvement_priority": priority
        }

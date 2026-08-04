"""
Candidate Resume Comparator
Compares two parsed profiles side-by-side to evaluate comparative scores and skill overlaps.
"""

from typing import Dict, Any, List
import pandas as pd

class ResumeComparator:
    """
    Evaluates candidate Candidate A vs Candidate B for recruiter decision support.
    """
    
    @staticmethod
    def compare_candidates(candA: Dict[str, Any], scoreA: Dict[str, Any],
                           candB: Dict[str, Any], scoreB: Dict[str, Any]) -> Dict[str, Any]:
        
        nameA = candA.get('name', 'Candidate A')
        nameB = candB.get('name', 'Candidate B')
        
        skillsA = set(candA.get('skills', []))
        skillsB = set(candB.get('skills', []))
        
        common_skills = sorted(list(skillsA.intersection(skillsB)))
        uniqueA = sorted(list(skillsA.difference(skillsB)))
        uniqueB = sorted(list(skillsB.difference(skillsA)))
        
        comparison_df = pd.DataFrame({
            "Dimension": ["Overall Score", "ATS Compatibility", "Completeness %", "Total Skills", "Projects Count", "Experience Blocks"],
            nameA: [
                scoreA.get('overall_score', 0),
                scoreA.get('ats_score', 0),
                scoreA.get('completeness_pct', 0),
                len(skillsA),
                len(candA.get('projects', [])),
                len(candA.get('experience', []))
            ],
            nameB: [
                scoreB.get('overall_score', 0),
                scoreB.get('ats_score', 0),
                scoreB.get('completeness_pct', 0),
                len(skillsB),
                len(candB.get('projects', [])),
                len(candB.get('experience', []))
            ]
        })
        
        winner = nameA if scoreA.get('overall_score', 0) >= scoreB.get('overall_score', 0) else nameB
        
        return {
            "nameA": nameA,
            "nameB": nameB,
            "comparison_df": comparison_df,
            "common_skills": common_skills,
            "uniqueA": uniqueA,
            "uniqueB": uniqueB,
            "winner": winner
        }

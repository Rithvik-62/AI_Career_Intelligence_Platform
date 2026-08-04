"""
Module for scoring a profile against a target job.
"""

def calculate_score(extracted_skills, required_skills):
    """
    Calculates a match score between extracted skills and required skills.
    """
    if not required_skills:
        return 0.0
        
    match_count = sum(1 for skill in required_skills if skill in extracted_skills)
    return (match_count / len(required_skills)) * 100

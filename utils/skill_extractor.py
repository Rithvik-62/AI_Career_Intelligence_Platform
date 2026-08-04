"""
Module for extracting skills from text using NLP.
"""
# pyrefly: ignore [missing-import]
import nltk

def extract_skills(text, predefined_skills=None):
    """
    Extracts skills from text.
    """
    if predefined_skills is None:
        predefined_skills = ["python", "machine learning", "data analysis", "sql", "java"]
        
    extracted = []
    text_lower = text.lower()
    for skill in predefined_skills:
        if skill in text_lower:
            extracted.append(skill)
    return extracted

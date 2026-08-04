"""
Job Description Match Engine
Performs text preprocessing, TF-IDF vectorization, Cosine Similarity, and skill intersection
to compute Candidate-Job Description alignment.
"""

from typing import Dict, Any, List
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.cleaner import clean_text
from utils.parser import ResumeParser

class JobDescriptionMatcher:
    """
    NLP & Vector Space module to measure candidate fit against a target job description.
    """
    
    DEFAULT_TECH_SKILLS = {
        'python', 'java', 'sql', 'javascript', 'react', 'node.js', 'html', 'css',
        'aws', 'docker', 'kubernetes', 'tensorflow', 'pytorch', 'pandas', 'scikit-learn',
        'machine learning', 'data science', 'full-stack', 'git', 'linux', 'c++', 'c#',
        'spring boot', 'express', 'mongodb', 'postgresql', 'mysql', 'power bi', 'tableau',
        'excel', 'spark', 'hadoop', 'nlp', 'deep learning', 'ci/cd', 'devops', 'azure', 'gcp'
    }
    
    def __init__(self):
        parsed_skills = set(ResumeParser().raw_skill_dict)
        self.skill_db = parsed_skills.union(self.DEFAULT_TECH_SKILLS)

    def _extract_skills_from_text(self, text: str) -> List[str]:
        text_lower = text.lower()
        extracted = []
        for skill in self.skill_db:
            pattern = r'(?<![\w])' + re.escape(skill) + r'(?![\w])'
            if re.search(pattern, text_lower):
                extracted.append(skill.title() if len(skill) > 2 else skill.upper())
        return sorted(list(set(extracted)))

    def match(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Executes TF-IDF Cosine Similarity and skill set intersection.
        """
        if not resume_text.strip() or not jd_text.strip():
            return {"error": "Both resume text and job description must be provided."}
            
        clean_resume = clean_text(resume_text)
        clean_jd = clean_text(jd_text)
        
        # 1. Cosine Similarity via TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
        similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        match_score = round(similarity * 100, 1)
        
        # 2. Skill Intersection Analysis
        resume_skills = set(self._extract_skills_from_text(resume_text))
        jd_skills = set(self._extract_skills_from_text(jd_text))
        
        matched_skills = sorted(list(resume_skills.intersection(jd_skills)))
        missing_skills = sorted(list(jd_skills.difference(resume_skills)))
        
        skill_coverage = round((len(matched_skills) / max(1, len(jd_skills))) * 100, 1) if jd_skills else 100.0
        employability_score = round((match_score * 0.5) + (skill_coverage * 0.5), 1)
        
        # 3. Recommendations
        recommendations = []
        if missing_skills:
            critical_missing = missing_skills[:3]
            recommendations.append(f"Add critical missing skills to your resume: {', '.join(critical_missing)}.")
        if match_score < 60:
            recommendations.append("Align the terminology in your resume bullet points closer to the job description keywords.")
        else:
            recommendations.append("Strong semantic match! Ensure your project section highlights achievements using these technologies.")
            
        return {
            "match_score": match_score,
            "skill_coverage": skill_coverage,
            "employability_score": employability_score,
            "resume_skills": sorted(list(resume_skills)),
            "jd_skills": sorted(list(jd_skills)),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "critical_missing": missing_skills[:5],
            "recommendations": recommendations
        }

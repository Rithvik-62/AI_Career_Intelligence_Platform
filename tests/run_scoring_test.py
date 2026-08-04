import sys
import json
import os
sys.path.append('.')
from utils.parser import ResumeParser
from utils.scoring import ResumeScorer

print("--- Running Scoring Tests ---")
parser = ResumeParser()
scorer = ResumeScorer()

resume_paths = [
    "dataset/external/test_ds.pdf",
    "dataset/external/test_se.pdf",
    "dataset/external/test_ba.pdf",
    "dataset/external/test_cy.pdf",
    "dataset/external/test_ce.pdf"
]

results = []
for path in resume_paths:
    print(f"\nEvaluating: {path}")
    parsed_data = parser.parse(path)
    score_result = scorer.score_resume(parsed_data)
    
    if "error" in score_result:
        print(f"Error: {score_result['error']}")
    else:
        print(f"Resume Name: {os.path.basename(path)}")
        print(f"Overall Score: {score_result['overall_score']}")
        print(f"Rating: {score_result['rating']}")
        print(f"Category Scores: {json.dumps(score_result['category_scores'])}")
        print("Suggestions:")
        for s in score_result['suggestions']:
            print(f"  - {s}")
            
        results.append({
            "resume": os.path.basename(path),
            "overall_score": score_result['overall_score'],
            "rating": score_result['rating'],
            "category_scores": score_result['category_scores'],
            "feedback": score_result['feedback'],
            "suggestions": score_result['suggestions']
        })

with open("scoring_test_results.json", "w") as f:
    json.dump(results, f, indent=4)

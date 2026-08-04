import sys
import json
import os
sys.path.append('.')

from utils.parser import ResumeParser
from utils.predictor import CareerPredictor
from utils.skill_gap import SkillGapAnalyzer

print("--- Running Skill Gap Tests ---")

parser = ResumeParser()
predictor = CareerPredictor()
analyzer = SkillGapAnalyzer()

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
    
    # 1. Parse
    parsed_data = parser.parse(path)
    
    # 2. Predict (This also parses internally but for this test we'll use predictor output)
    pred_result = predictor.predict(path)
    
    if "error" in pred_result:
        print(f"Prediction Error: {pred_result['error']}")
        continue
        
    predicted_role = pred_result['predicted_role']
    print(f"Predicted Career: {predicted_role}")
    
    # 3. Analyze Skill Gap
    gap_analysis = analyzer.analyze(parsed_data, predicted_role)
    
    if "error" in gap_analysis:
        print(f"Gap Error: {gap_analysis['error']}")
        continue
        
    print(f"Matching Skills: {gap_analysis['matching_skills']}")
    print(f"Missing Skills: {gap_analysis['missing_skills']}")
    print(f"Coverage %: {gap_analysis['coverage_percentage']}%")
    print(f"Career Readiness: {gap_analysis['readiness_level']}")
    print("Roadmap:")
    for step in gap_analysis['learning_roadmap']:
        print(f"  - {step}")
        
    results.append({
        "resume": os.path.basename(path),
        "predicted_role": predicted_role,
        "gap_analysis": gap_analysis
    })

with open("skill_gap_test_results.json", "w") as f:
    json.dump(results, f, indent=4)

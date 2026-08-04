import sys
import json
import os
sys.path.append('.')
from utils.predictor import CareerPredictor
from reportlab.pdfgen import canvas

def create_resume(path, title, keywords):
    c = canvas.Canvas(path)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Candidate Name")
    c.setFont("Helvetica", 12)
    c.drawString(50, 780, "Candidate Email | 555-555-5555")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 740, "EXPERIENCE")
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Senior {title} at Example Inc (2018 - Present)")
    c.drawString(50, 700, f"Developed systems utilizing {keywords}.")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 660, "SKILLS")
    c.setFont("Helvetica", 12)
    c.drawString(50, 640, f"Proficient in {keywords}.")
    
    c.save()

os.makedirs('dataset/external', exist_ok=True)

resumes = [
    ("dataset/external/test_ds.pdf", "Data Scientist", "Python, Pandas, NumPy, Scikit-learn, Machine Learning, Deep Learning, PyTorch, SQL, Statistics"),
    ("dataset/external/test_se.pdf", "Software Developer", "Java, C++, C#, Git, Agile, JavaScript, Node.js, React, APIs, Docker, Linux, CI/CD"),
    ("dataset/external/test_ba.pdf", "Business Analyst", "Excel, Power BI, Tableau, SQL, Stakeholder Management, Requirements Gathering, Agile, Jira"),
    ("dataset/external/test_cy.pdf", "Cyber Security Analyst", "Linux, Network Security, Firewalls, Wireshark, Penetration Testing, Risk Assessment, Encryption"),
    ("dataset/external/test_ce.pdf", "Cloud Engineer", "AWS, Azure, GCP, Docker, Kubernetes, Terraform, Cloud Architecture, Linux, CI/CD")
]

for path, title, keywords in resumes:
    create_resume(path, title, keywords)
    print(f"Created {path}")

print("\n--- Running Predictions ---")
predictor = CareerPredictor()

results = []
for path, title, keywords in resumes:
    print(f"\nEvaluating: {path} (Expected: {title})")
    try:
        # To display extracted resume length, we can load PDF text using parser
        text = predictor.parser._extract_text_from_pdf(path)
        length = len(text.split())
    except:
        length = 0
        
    res = predictor.predict(path)
    
    print(f"Extracted Length: {length} words")
    
    if "error" in res:
        print(f"Error: {res['error']}")
    else:
        print(f"Predicted Career: {res['predicted_role']}")
        print(f"Confidence: {res['confidence']}%")
        print("Top 3 Predictions:")
        for top in res['top_predictions']:
            print(f"  - {top['role']}: {top['confidence']}%")
        
        # Save output for notebook usage
        results.append({
            "file": os.path.basename(path),
            "expected": title,
            "length": length,
            "prediction": res['predicted_role'],
            "confidence": res['confidence'],
            "top_3": res['top_predictions']
        })

with open("prediction_test_results.json", "w") as f:
    json.dump(results, f, indent=4)

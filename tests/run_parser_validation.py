import os
import sys
import json
import glob

sys.path.append('.') # To allow importing utils
from utils.parser import ResumeParser

def generate_report(results, report_path):
    total = len(results)
    if total == 0:
        return
        
    avg_confidence = sum(r['confidence'] for r in results) / total
    
    # Check if section exists in parsed output
    has_skills = sum(1 for r in results if r['skills_count'] > 0)
    has_experience = sum(1 for r in results if r['experience_count'] > 0)
    has_education = sum(1 for r in results if r['education_count'] > 0)
    has_projects = sum(1 for r in results if r['projects_count'] > 0)
    
    with open(report_path, "w") as f:
        f.write("# Parsing Accuracy Report\n\n")
        f.write(f"**Total Resumes Tested:** {total}\n")
        f.write(f"**Average Confidence Score:** {avg_confidence:.2f}%\n\n")
        
        f.write("## Section Detection Rates\n")
        f.write(f"- **Skills:** {(has_skills/total)*100:.1f}%\n")
        f.write(f"- **Experience:** {(has_experience/total)*100:.1f}%\n")
        f.write(f"- **Education:** {(has_education/total)*100:.1f}%\n")
        f.write(f"- **Projects:** {(has_projects/total)*100:.1f}%\n\n")
        
        f.write("## Examples of Parsed Structure\n")
        for i, res in enumerate(results):
            f.write(f"### {res['file']}\n")
            f.write(f"- **Name:** {res['name']}\n")
            f.write(f"- **Email:** {res['email']}\n")
            f.write(f"- **Phone:** {res['phone']}\n")
            f.write(f"- **Portfolio:** {res['portfolio']}\n")
            f.write(f"- **Location:** {res['location']}\n")
            f.write(f"- **Skills Count:** {res['skills_count']} (e.g. {', '.join(res['skills'][:3])}...)\n")
            f.write(f"- **Experience Blocks:** {res['experience_count']}\n")
            if res['experience_count'] > 0:
                exp = res['experience_blocks'][0]
                title = exp.get('job_title', 'Unknown')
                dates = exp.get('dates', 'Unknown')
                f.write(f"  - *Sample:* {title} ({dates})\n")
            f.write(f"- **Projects Blocks:** {res['projects_count']}\n\n")

def main():
    print("=== STARTING PARSER VALIDATION ON REAL RESUMES ===")
    
    pdf_files = glob.glob('Sample_Resume/*.pdf')
    if not pdf_files:
        print("No PDF files found in Sample_Resume directory!")
        return
        
    os.makedirs('logs', exist_ok=True)
    
    parser = ResumeParser()
    results = []
    
    for pdf_path in pdf_files:
        print(f"\nProcessing {os.path.basename(pdf_path)}...")
        
        parsed = parser.parse(pdf_path)
        
        if "error" in parsed:
            print(f"Error parsing resume {pdf_path}: {parsed['error']}")
            continue
            
        conf = parsed.get("metadata", {}).get("parsing_confidence", 0.0)
        
        results.append({
            "file": os.path.basename(pdf_path),
            "name": parsed.get("name"),
            "email": parsed.get("email"),
            "phone": parsed.get("phone"),
            "location": parsed.get("location"),
            "portfolio": parsed.get("portfolio"),
            "confidence": conf,
            "skills_count": len(parsed.get("skills", [])),
            "skills": parsed.get("skills", []),
            "experience_count": len(parsed.get("experience", [])),
            "experience_blocks": parsed.get("experience", []),
            "education_count": len(parsed.get("education", [])),
            "projects_count": len(parsed.get("projects", []))
        })
        
        print(f"Conf={conf}%, Skills={len(parsed.get('skills',[]))}, Exp={len(parsed.get('experience',[]))}")

    report_path = "C:/Users/RITHVIK/.gemini/antigravity-ide/brain/8275ec1b-0877-4169-9623-09c354bcea30/parsing_accuracy_report.md"
    generate_report(results, report_path)
    print(f"\nParsing validation complete. Report saved to {report_path}")

if __name__ == "__main__":
    main()

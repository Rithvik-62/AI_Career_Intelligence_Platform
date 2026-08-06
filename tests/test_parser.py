"""
Comprehensive Resume Parser Verification Test Suite
Tests ResumeParser accuracy across all sample PDF templates.
"""

import os
import sys
import glob
from typing import Dict, Any

sys.path.append(os.getcwd())
from utils.parser import ResumeParser


def run_parser_validation():
    parser = ResumeParser()
    sample_dir = os.path.join(os.getcwd(), 'Sample_Resume')
    pdf_files = sorted(glob.glob(os.path.join(sample_dir, '*.pdf')))

    print("=" * 80)
    print(f"RESUME PARSER VALIDATION TEST -- {len(pdf_files)} SAMPLE RESUMES")
    print("=" * 80)

    results = []
    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        print(f"\nTesting File: {file_name}")
        
        parsed = parser.parse(pdf_path)
        
        name = parsed.get("name")
        email = parsed.get("email")
        phone = parsed.get("phone")
        location = parsed.get("location")
        linkedin = parsed.get("linkedin")
        github = parsed.get("github")
        portfolio = parsed.get("portfolio")
        skills = parsed.get("skills", [])
        experience = parsed.get("experience", [])
        education = parsed.get("education", [])
        projects = parsed.get("projects", [])
        confidence = parsed.get("metadata", {}).get("parsing_confidence", 0)

        print(f"  Candidate Name : {name}")
        print(f"  Email Address  : {email}")
        print(f"  Phone Number   : {phone}")
        print(f"  Location       : {location}")
        print(f"  LinkedIn       : {linkedin}")
        print(f"  GitHub         : {github}")
        print(f"  Portfolio      : {portfolio}")
        print(f"  Skills ({len(skills)}): {skills[:6]}")
        print(f"  Experience Count: {len(experience)}")
        print(f"  Education Count : {len(education)}")
        print(f"  Projects Count  : {len(projects)}")
        print(f"  Parsing Confidence: {confidence:.1f}%")

        # Validation checks
        has_name = name not in [None, "Name Not Detected", ""]
        has_email = email not in [None, "Email Not Found", ""]
        has_skills = len(skills) > 0

        status = "PASSED [OK]" if (has_name and has_skills) else "NEEDS FIX [FAIL]"
        print(f"  Result Status: {status}")

        results.append({
            "file": file_name,
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "skills_count": len(skills),
            "exp_count": len(experience),
            "edu_count": len(education),
            "confidence": confidence,
            "status": status
        })

    print("\n" + "=" * 80)
    print("SUMMARY RESULTS")
    print("=" * 80)
    passed_cnt = sum(1 for r in results if r["status"] == "PASSED [OK]")
    print(f"Passed: {passed_cnt}/{len(results)} resumes parsed successfully.")
    return results


if __name__ == "__main__":
    run_parser_validation()

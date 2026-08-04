import pandas as pd
import json
import sys
import os
import io
sys.path.append('.') # To allow importing utils
from utils.cleaner import clean_text

def run_preprocessing():
    # Load Dataset
    print("=== STEP 1: Load Raw Dataset ===")
    
    with open('dataset/raw/Resume.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('\ufeff'):
            line = line[1:]
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        cleaned_lines.append(line)

    data = '\n'.join(cleaned_lines)
    
    try:
        df = pd.read_csv(io.StringIO(data))
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # STEP 1.5: Clean out malformed rows
    initial_count = len(df)
    
    # Drop rows where category is a float string (like '0.0', '37.0')
    df = df[~df['category'].astype(str).str.match(r'^\d+\.\d+$', na=False)]
    
    # Drop rows missing resume_text or category
    df = df.dropna(subset=['resume_text', 'category'])
    
    # Drop duplicate resumes
    df = df.drop_duplicates(subset=['resume_text'])
    
    # STEP 2: CATEGORY MAPPING
    print("=== STEP 2: Category Mapping ===")
    
    category_mapping = {
        "INFORMATION-TECHNOLOGY": "Software Developer",
        "Python Developer": "Software Developer",
        "Java Developer": "Software Developer",
        "DotNet Developer": "Software Developer",
        "SAP Developer": "Software Developer",
        "Automation Testing": "Software Developer",
        "Testing": "Software Developer",
        "Mobile App Developer (iOS/Android)": "Software Developer",
        "Blockchain": "Software Developer",
        "Frontend Developer": "Web Developer",
        "Backend Developer": "Web Developer",
        "Full Stack Developer": "Web Developer",
        "Web Designing": "Web Developer",
        "Data Science": "Data Scientist",
        "Database": "Database Administrator",
        "Network Security Engineer": "Cyber Security Analyst",
        "ETL Developer": "Data Engineer",
        "Hadoop": "Data Engineer",
        "DevOps Engineer": "Cloud Engineer"
    }

    keep_exact = [
        "Data Scientist",
        "Cloud Engineer",
        "Machine Learning Engineer",
        "Business Analyst",
        "Software Developer", 
        "Web Developer",
        "Database Administrator",
        "Cyber Security Analyst",
        "Data Engineer",
        "Data Analyst", # Just in case
        "AI Engineer"   # Just in case
    ]

    # Map categories
    df['mapped_category'] = df['category'].replace(category_mapping)
    
    # Keep only supported
    df = df[df['mapped_category'].isin(keep_exact)]
    
    print(f"Rows after mapping and filtering: {len(df)}")
    
    # Apply Cleaning
    print("\n=== STEP 3: Apply Preprocessing ===")
    df['Cleaned_Resume'] = df['resume_text'].apply(clean_text)

    # Validate Results
    print("\n=== STEP 4: Quality Checks ===")
    empty_cleaned = (df['Cleaned_Resume'] == '').sum()
    null_cleaned = df['Cleaned_Resume'].isnull().sum()
    duplicate_cleaned = df.duplicated(subset=['Cleaned_Resume']).sum()

    print(f"No empty cleaned resumes: {'Yes' if empty_cleaned == 0 else 'No (' + str(empty_cleaned) + ')'}")
    print(f"No null values: {'Yes' if null_cleaned == 0 else 'No (' + str(null_cleaned) + ')'}")

    report = {
        "original_rows": initial_count,
        "removed_rows": initial_count - len(df),
        "final_rows": len(df),
        "class_distribution": df['mapped_category'].value_counts().to_dict(),
        "empty_cleaned": int(empty_cleaned),
        "null_cleaned": int(null_cleaned)
    }

    os.makedirs('logs', exist_ok=True)
    with open("logs/dataset_cleaning_summary.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print(json.dumps(report, indent=4))

    # Save Dataset
    print("\n=== STEP 5: Save Dataset ===")
    os.makedirs('dataset/processed', exist_ok=True)
    
    # Save as clean_resume_dataset.csv 
    # (Including resume_text, mapped_category, skills_list, experience_years)
    df_to_save = df[['resume_text', 'mapped_category', 'skills_list', 'experience_years', 'Cleaned_Resume']]
    df_to_save.to_csv('dataset/processed/clean_resume_dataset.csv', index=False)
    
    print("Saved to dataset/processed/clean_resume_dataset.csv")

if __name__ == "__main__":
    run_preprocessing()

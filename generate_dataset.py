import pandas as pd
import numpy as np
import urllib.request
import io
import json
import os

# Create directories if they don't exist
os.makedirs("dataset/raw", exist_ok=True)
os.makedirs("dataset/processed", exist_ok=True)
os.makedirs("dataset/external", exist_ok=True)

target_categories = [
    "Data Analyst", "Business Analyst", "Data Scientist", "Machine Learning Engineer",
    "AI Engineer", "Software Developer", "Web Developer", "Cloud Engineer", 
    "Data Engineer", "Cyber Security Analyst", "Database Administrator"
]

np.random.seed(42)

skills_dict = {
    "Data Analyst": ["SQL", "Excel", "Tableau", "Power BI", "Python", "Data Visualization", "Statistics", "Pandas"],
    "Business Analyst": ["Requirements Gathering", "Agile", "SQL", "Excel", "JIRA", "Process Modeling", "Stakeholder Management"],
    "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "NLP", "Scikit-Learn", "TensorFlow", "Statistics", "R", "SQL"],
    "Machine Learning Engineer": ["Python", "Scikit-Learn", "TensorFlow", "PyTorch", "Model Deployment", "MLOps", "Docker", "AWS"],
    "AI Engineer": ["Deep Learning", "NLP", "Computer Vision", "PyTorch", "OpenAI", "LLMs", "Generative AI", "Python"],
    "Software Developer": ["Java", "Python", "C++", "C#", "Data Structures", "Algorithms", "Git", "Spring Boot", "REST APIs"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "MongoDB", "TypeScript", "Tailwind CSS"],
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Linux", "Networking"],
    "Data Engineer": ["Python", "SQL", "Spark", "Hadoop", "Airflow", "Kafka", "ETL", "AWS Redshift", "Snowflake"],
    "Cyber Security Analyst": ["Network Security", "Penetration Testing", "Ethical Hacking", "Firewalls", "SIEM", "Linux", "Cryptography"],
    "Database Administrator": ["SQL Server", "Oracle", "MySQL", "PostgreSQL", "Database Tuning", "Backup & Recovery", "NoSQL"]
}

synthetic_data = []

# Generate dataset
for category in target_categories:
    # 200 records per category
    for i in range(200):
        num_skills = np.random.randint(4, 9)
        cat_skills = skills_dict[category]
        selected_skills = np.random.choice(cat_skills, min(num_skills, len(cat_skills)), replace=False).tolist()
        
        all_skills = [skill for sublist in skills_dict.values() for skill in sublist]
        noise_skills = np.random.choice(all_skills, 2, replace=False).tolist()
        
        final_skills = list(set(selected_skills + noise_skills))
        np.random.shuffle(final_skills)
        
        resume_text = f"Experienced professional skilled in {', '.join(final_skills)}. Proven track record in delivering high-quality results. Seeking a challenging role as a {category}."
        
        # Add missing values randomly (5% chance)
        if np.random.rand() < 0.05:
            resume_text = np.nan
            
        synthetic_data.append({
            "Resume_Text": resume_text,
            "Role": category
        })

df_synthetic = pd.DataFrame(synthetic_data)

# Inject some duplicates (e.g. 50 duplicate rows)
duplicates_to_add = df_synthetic.sample(50, random_state=42)
df_synthetic = pd.concat([df_synthetic, duplicates_to_add], ignore_index=True)

# Shuffle dataset
df_synthetic = df_synthetic.sample(frac=1, random_state=42).reset_index(drop=True)

# Save raw
df_synthetic.to_csv("dataset/raw/resume_dataset.csv", index=False)

# Get metrics before cleaning
missing = df_synthetic.isnull().sum().to_dict()
duplicates = int(df_synthetic.duplicated().sum())

# Cleaning steps for 'processed'
df_cleaned = df_synthetic.dropna()
df_cleaned = df_cleaned.drop_duplicates()

# Save processed
df_cleaned.to_csv("dataset/processed/career_dataset.csv", index=False)

summary = {
    "rows_raw": len(df_synthetic),
    "columns": len(df_synthetic.columns),
    "column_names": list(df_synthetic.columns),
    "data_types": {k: str(v) for k, v in df_synthetic.dtypes.items()},
    "missing_values": missing,
    "duplicates": duplicates,
    "target_variable": "Role",
    "rows_cleaned": len(df_cleaned)
}

with open("dataset_summary.json", "w") as f:
    json.dump(summary, f)

print("success")

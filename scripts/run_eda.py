import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json
import os

# Create images folder if not exists
os.makedirs("images", exist_ok=True)
artifact_dir = r"C:\Users\RITHVIK\.gemini\antigravity-ide\brain\8275ec1b-0877-4169-9623-09c354bcea30"

# Step 1: Load Dataset
df = pd.read_csv("dataset/processed/preprocessed_resume_dataset.csv")

# Step 4 & 8 prep: Create numerical features
df['Resume_Length'] = df['Cleaned_Resume'].apply(lambda x: len(str(x).split()))
df['Char_Count'] = df['Cleaned_Resume'].apply(lambda x: len(str(x)))
df['Avg_Word_Length'] = df['Char_Count'] / df['Resume_Length']

# Save EDA dataset
df.to_csv("dataset/processed/eda_resume_dataset.csv", index=False)

# Visualizations setup
plt.style.use('ggplot')
colors = plt.cm.tab20.colors

# 1. Target Variable Bar Chart
plt.figure(figsize=(12, 6))
role_counts = df['Role'].value_counts()
role_counts.plot(kind='bar', color=colors[:len(role_counts)])
plt.title('Distribution of Career Roles')
plt.xlabel('Role')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "role_bar_chart.png"))
plt.close()

# 2. Target Variable Pie Chart
plt.figure(figsize=(10, 8))
role_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=colors[:len(role_counts)])
plt.title('Percentage Distribution of Career Roles')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "role_pie_chart.png"))
plt.close()

# 3. Resume Length Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Resume_Length'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Resume Length (Word Count)')
plt.xlabel('Number of Words')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "length_histogram.png"))
plt.close()

# 4. Resume Length Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Resume_Length'], color='lightgreen')
plt.title('Box Plot of Resume Length')
plt.xlabel('Number of Words')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "length_boxplot.png"))
plt.close()

# 5. Resume Length by Role (Box Plot) - Extra visualization
plt.figure(figsize=(12, 6))
sns.boxplot(x='Role', y='Resume_Length', data=df, palette='Set3')
plt.title('Resume Length Distribution by Role')
plt.xlabel('Role')
plt.ylabel('Number of Words')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "length_by_role_boxplot.png"))
plt.close()

# 6. Correlation Matrix Heatmap
plt.figure(figsize=(8, 6))
corr = df[['Resume_Length', 'Char_Count', 'Avg_Word_Length']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix of Numerical Features')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "correlation_heatmap.png"))
plt.close()

# Word Frequency Analysis
all_words = ' '.join(df['Cleaned_Resume'].dropna()).split()
word_counts = Counter(all_words)
top_30_words = word_counts.most_common(30)
words, counts = zip(*top_30_words)

# 7. Word Frequency Horizontal Bar Chart
plt.figure(figsize=(12, 8))
plt.barh(words[::-1], counts[::-1], color='coral')
plt.title('Top 30 Most Frequent Words in Resumes')
plt.xlabel('Frequency')
plt.ylabel('Words')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "word_freq_bar.png"))
plt.close()

# Specific Skill Extraction (Mock specific skills from the given list)
technical_skills = ['python', 'java', 'sql', 'excel', 'power bi', 'tableau', 'aws', 'tensorflow', 'pytorch', 'machine learning', 'statistics', 'pandas', 'numpy', 'scikit-learn', 'git', 'react', 'node.js', 'docker', 'kubernetes', 'azure', 'gcp', 'linux', 'c++', 'c#']

skill_counts = {skill: 0 for skill in technical_skills}
for resume in df['Cleaned_Resume'].dropna():
    for skill in technical_skills:
        if skill in resume:
            skill_counts[skill] += 1

top_20_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20]
skills, s_counts = zip(*top_20_skills)

# 8. Top 20 Technical Skills Horizontal Bar Chart
plt.figure(figsize=(12, 8))
plt.barh(skills[::-1], s_counts[::-1], color='mediumpurple')
plt.title('Top 20 Technical Skills Extracted')
plt.xlabel('Frequency')
plt.ylabel('Skills')
plt.tight_layout()
plt.savefig(os.path.join(artifact_dir, "top_skills_bar.png"))
plt.close()

# Role-wise skills
role_skills = {}
for role in df['Role'].unique():
    role_df = df[df['Role'] == role]
    r_words = ' '.join(role_df['Cleaned_Resume'].dropna()).split()
    r_counts = Counter(r_words)
    # Filter for tech skills
    r_tech = {k: v for k, v in r_counts.items() if k in technical_skills}
    top_3 = [k for k, v in sorted(r_tech.items(), key=lambda x: x[1], reverse=True)[:3]]
    role_skills[role] = ", ".join(top_3)

with open("role_skills.json", "w") as f:
    json.dump(role_skills, f)

print("EDA script completed successfully.")

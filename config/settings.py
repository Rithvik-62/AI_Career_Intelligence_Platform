import os

# Base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATASET_RAW_DIR = os.path.join(BASE_DIR, 'dataset', 'raw')
DATASET_PROCESSED_DIR = os.path.join(BASE_DIR, 'dataset', 'processed')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
TEMP_DIR = os.path.join(BASE_DIR, 'temp_pdfs')

# Ensure necessary directories exist
for directory in [LOGS_DIR, TEMP_DIR, MODELS_DIR, DATASET_RAW_DIR, DATASET_PROCESSED_DIR]:
    os.makedirs(directory, exist_ok=True)

# Model Paths
MODEL_PATH = os.path.join(MODELS_DIR, 'career_model.pkl') 
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl') 
LABEL_ENCODER_PATH = os.path.join(MODELS_DIR, 'label_encoder.pkl')

# Dataset Paths
CLEAN_RESUME_DATASET = os.path.join(DATASET_PROCESSED_DIR, 'clean_resume_dataset.csv')
PREPROCESSED_RESUME_DATASET = os.path.join(DATASET_PROCESSED_DIR, 'preprocessed_resume_dataset.csv')
RAW_RESUME_DATASET = os.path.join(DATASET_RAW_DIR, 'Resume.csv')

# Application Constants
APP_NAME = "AI Career Intelligence Platform"
VERSION = "2.0.0"
MIN_PYTHON_VERSION = (3, 11)
MAX_TESTED_PYTHON_VERSION = (3, 12)

# Supported Tech Careers mapping (11 approved classes)
SUPPORTED_CAREERS = [
    "Data Analyst",
    "Data Scientist",
    "Business Analyst",
    "Software Developer",
    "Cloud Engineer",
    "AI Engineer",
    "Cyber Security Analyst",
    "DevOps Engineer",
    "Database Administrator",
    "Network Engineer",
    "Web Developer"
]

# Baseline Career Requirement Database
CAREER_DATABASE = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Pandas", "PyTorch", "TensorFlow", "Scikit-Learn", "Statistics"],
    "Machine Learning Engineer": ["Python", "PyTorch", "TensorFlow", "Docker", "Kubernetes", "MLOps", "Git", "SQL"],
    "Software Developer": ["Java", "Python", "JavaScript", "SQL", "Git", "Docker", "REST API", "OOP", "Data Structures"],
    "Web Developer": ["JavaScript", "React", "HTML", "CSS", "Node.js", "TypeScript", "Git", "REST API"],
    "Data Analyst": ["SQL", "Excel", "Power BI", "Python", "Tableau", "Statistics", "Data Visualization"],
    "Business Analyst": ["SQL", "Excel", "Power BI", "Requirements Gathering", "Agile", "Process Mapping", "Tableau"],
    "Cloud Engineer": ["AWS", "Terraform", "Docker", "Kubernetes", "Linux", "Python", "Networking", "Security"],
    "DevOps Engineer": ["Docker", "Kubernetes", "Jenkins", "Terraform", "Git", "Linux", "Python", "CI/CD"],
    "Cyber Security Analyst": ["Networking", "Linux", "Python", "SIEM", "Firewalls", "Cryptography", "Risk Assessment"],
    "Database Administrator": ["SQL", "PostgreSQL", "MySQL", "Oracle", "Database Indexing", "Backup & Recovery", "Linux"],
    "Network Engineer": ["Networking", "Cisco", "Firewalls", "TCP/IP", "VPN", "Linux", "Python", "Routing & Switching"]
}

# Common Skill Dictionary for normalization
SKILL_MAPPING = {
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "ms sql": "SQL Server",
    "sql server": "SQL Server",
    "reactjs": "React",
    "react.js": "React",
    "vuejs": "Vue.js",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "aws": "AWS",
    "gcp": "Google Cloud",
    "azure": "Azure",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "cv": "Computer Vision"
}

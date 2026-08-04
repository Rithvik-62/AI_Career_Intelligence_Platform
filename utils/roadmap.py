"""
Career Database Module
Stores required skills, certifications, projects, and interview topics for each supported career.
"""

CAREER_DATABASE = {
    "Data Analyst": {
        "required_skills": ["python", "sql", "excel", "power bi", "statistics", "tableau", "pandas"],
        "certifications": [
            "Microsoft Power BI Data Analyst",
            "Google Data Analytics",
            "Tableau Desktop Specialist"
        ],
        "projects": [
            "Sales Dashboard",
            "HR Analytics",
            "Customer Churn Analysis"
        ],
        "interview_topics": [
            "SQL Querying",
            "Data Visualization Best Practices",
            "Statistical Testing",
            "Business Case Studies",
            "Excel Advanced Functions"
        ]
    },
    "Data Scientist": {
        "required_skills": ["python", "machine learning", "statistics", "pandas", "numpy", "scikit-learn", "deep learning"],
        "certifications": [
            "AWS Certified Machine Learning",
            "IBM Data Science Professional",
            "Google Professional Data Engineer"
        ],
        "projects": [
            "Predictive Maintenance Model",
            "Recommender System",
            "Fraud Detection Algorithm"
        ],
        "interview_topics": [
            "Machine Learning Algorithms",
            "Probability and Statistics",
            "Feature Engineering",
            "Model Deployment",
            "A/B Testing"
        ]
    },
    "AI Engineer": {
        "required_skills": ["python", "tensorflow", "pytorch", "deep learning", "computer vision", "nlp", "aws"],
        "certifications": [
            "TensorFlow Developer Certificate",
            "AWS Machine Learning Specialty",
            "DeepLearning.AI Certifications"
        ],
        "projects": [
            "Image Classification System",
            "Custom Chatbot (NLP)",
            "Real-time Object Detection"
        ],
        "interview_topics": [
            "Deep Learning Architectures",
            "Transformers and Attention",
            "Model Optimization",
            "Gradient Descent Math",
            "MLOps"
        ]
    },
    "Software Developer": {
        "required_skills": ["java", "python", "git", "oop", "sql", "rest api", "testing", "javascript"],
        "certifications": [
            "Oracle Certified Professional",
            "AWS Certified Developer",
            "Microsoft Certified: Azure Developer"
        ],
        "projects": [
            "E-commerce Website",
            "Task Manager Application",
            "Inventory System API"
        ],
        "interview_topics": [
            "Data Structures & Algorithms",
            "Object-Oriented Design",
            "System Design Basics",
            "RESTful Principles",
            "Database Indexing"
        ]
    },
    "Cloud Engineer": {
        "required_skills": ["aws", "azure", "gcp", "docker", "kubernetes", "linux", "terraform", "ci/cd"],
        "certifications": [
            "AWS Solutions Architect Associate",
            "Microsoft Azure Fundamentals",
            "Google Cloud Associate Cloud Engineer"
        ],
        "projects": [
            "Highly Available Web App Deployment",
            "Infrastructure as Code Automation",
            "Serverless API Backend"
        ],
        "interview_topics": [
            "Cloud Networking",
            "Container Orchestration",
            "IAM and Security",
            "High Availability Architecture",
            "Linux Troubleshooting"
        ]
    },
    "Business Analyst": {
        "required_skills": ["excel", "power bi", "tableau", "sql", "stakeholder management", "agile", "jira"],
        "certifications": [
            "Certified Business Analysis Professional (CBAP)",
            "PMI Professional in Business Analysis (PMI-PBA)",
            "Agile Analysis Certification (AAC)"
        ],
        "projects": [
            "Market Expansion Feasibility Study",
            "Process Optimization Blueprint",
            "Financial Forecasting Model"
        ],
        "interview_topics": [
            "Requirements Elicitation",
            "Stakeholder Management",
            "Agile Frameworks",
            "Process Modeling",
            "Data-Driven Decision Making"
        ]
    },
    "Cyber Security Analyst": {
        "required_skills": ["linux", "network security", "firewalls", "wireshark", "penetration testing", "risk assessment", "encryption"],
        "certifications": [
            "CompTIA Security+",
            "Certified Ethical Hacker (CEH)",
            "Certified Information Systems Security Professional (CISSP)"
        ],
        "projects": [
            "Network Traffic Analyzer",
            "Vulnerability Assessment Report",
            "Simulated Phishing Campaign"
        ],
        "interview_topics": [
            "OSI Model & Networking",
            "Common Cyber Attacks (XSS, SQLi)",
            "Cryptography Basics",
            "Incident Response Lifecycles",
            "Security Frameworks (NIST)"
        ]
    }
}

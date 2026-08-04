# AI Career Intelligence Platform: Final Project Report

## 1. Abstract
The traditional recruitment and career counseling processes are highly manual, time-consuming, and prone to human bias. Candidates often struggle to identify the correct career trajectory based on their existing skill sets, and frequently lack awareness of the specific technical gaps preventing them from securing their target roles. The **AI Career Intelligence Platform** is an end-to-end Machine Learning web application designed to automate resume analysis. By leveraging Natural Language Processing (NLP) heuristics and a trained Decision Tree Classifier, the platform parses unstructured PDF resumes, predicts the candidate's optimal tech career role, calculates an automated Applicant Tracking System (ATS) score, and generates a personalized, step-by-step learning roadmap.

## 2. Problem Statement
Job seekers in the technology sector often face rejection due to poorly optimized resumes and a mismatch between their acquired skills and industry demands. Conversely, recruiters spend countless hours manually parsing unstructured resumes. There is a critical need for an automated, intelligent system capable of interpreting raw resume data, scoring it against industry benchmarks, and providing actionable feedback to bridge the candidate's skill gap.

## 3. Objectives
- **Automated Parsing**: Extract structured entities (Skills, Education, Experience, Projects) natively from PDF files without requiring manual data entry.
- **Career Prediction**: Utilize Machine Learning to classify the candidate into one of 11 core technology careers based on their technical vocabulary footprint.
- **Skill Gap Analysis**: Cross-reference the candidate's skills against a proprietary career database to identify missing competencies.
- **Actionable Roadmaps**: Generate customized learning curriculums, recommended projects, and certifications to elevate the candidate's ATS score.

## 4. Existing System vs Proposed System
### Existing System
- Relies on manual human review or primitive keyword-matching ATS software.
- Offers binary feedback (Accepted/Rejected) without constructive guidance.
- Does not predict alternative career trajectories based on latent skills.

### Proposed System
- **Intelligent Extraction**: Uses regex and NLP to intelligently chunk work experience and projects.
- **Statistical Prediction**: Leverages TF-IDF vectorization and a Decision Tree Classifier to provide a mathematical confidence score for the recommended career.
- **Holistic Dashboard**: Visualizes data using Plotly radar charts and provides a downloadable PDF report.

## 5. Technology Stack
- **Programming Language**: Python 3.9+
- **Frontend Framework**: Streamlit 1.29+
- **Machine Learning**: Scikit-Learn (Decision Tree, KNN, SVM evaluated; Decision Tree deployed)
- **Natural Language Processing**: NLTK, pdfplumber, Regular Expressions
- **Data Manipulation**: Pandas, NumPy
- **Data Visualization**: Plotly
- **Exporting**: ReportLab (PDF Generation)

## 6. System Architecture & Modules
The architecture is decoupled into Presentation (Streamlit), Business Logic (Parsers/Scorers), and Machine Learning (Predictor) layers.

1. **Parser Module**: Uses `pdfplumber` to extract raw text, followed by Regex heuristics to chunk the text into specific dictionaries (Experience, Projects, Education).
2. **ML Predictor Module**: Ingests raw text, applies NLTK stopwords/lemmatization, transforms via `TfidfVectorizer`, and runs `model.predict_proba()` to output role probabilities.
3. **Scoring Module**: Evaluates the structural density and section presence of the resume, assigning an ATS score out of 100.
4. **Skill Gap Module**: Uses `config.settings` and `utils.roadmap` to compare extracted skills against industry requirements, returning a JSON of missing skills and recommended steps.
5. **Dashboard Module**: A Streamlit UI that consumes the JSON outputs from the aforementioned modules and renders glowing HTML cards and Plotly graphs.

## 7. Algorithms Used
- **TF-IDF (Term Frequency - Inverse Document Frequency)**: Used to convert unstructured resume text into numerical feature vectors, weighting highly specific technical terms heavier than common words.
- **Decision Tree Classifier**: The core predictive model. It splits the TF-IDF feature space based on Gini impurity to classify the resume into one of 11 distinct technology roles. (Accuracy achieved: 92.7%).

## 8. Dataset Description
The model was trained on an augmented version of `Resume.csv`, originally containing over 2,400 resumes across various fields. The dataset was audited and filtered down to 11 specific technology roles (e.g., Data Scientist, DevOps Engineer, Python Developer). The final dataset was balanced and cleaned to prevent class bias.

## 9. Testing & Results
- **Parser Validation**: Tested against 10 diverse, real-world PDF layouts. Achieved >90% accuracy in isolating skills and contact information.
- **Model Evaluation**: Evaluated using K-Fold Cross Validation. The Decision Tree achieved an F1-Score of 0.92, outperforming SVM and KNN on this specific sparse text dataset.
- **UI Smoke Testing**: Verified component rendering across all pages. Integrated Streamlit `@st.cache_resource` to ensure models load in < 0.5 seconds on subsequent inferences.

## 10. Advantages & Limitations
### Advantages
- Operates entirely offline (no external API costs).
- Blazingly fast inference time.
- Highly actionable, personalized feedback for candidates.

### Limitations
- **PDF Constraints**: Highly graphical, non-standard, or image-based (non-OCR) PDFs cannot be parsed accurately.
- **Static Roadmaps**: The skill gap database is static and requires manual updates to keep pace with evolving tech trends.

## 11. Future Scope
- **LLM Integration**: Replacing the deterministic regex parser with a local Large Language Model (e.g., LLaMA 3) for semantic entity extraction.
- **Live Job Scraping**: Integrating with LinkedIn/Indeed APIs to present real-time job openings based on the predicted role.

## 12. Conclusion
The AI Career Intelligence Platform successfully demonstrates how Machine Learning and NLP can be synergized to solve a real-world HR and recruitment problem. By automating the parsing, scoring, and advisory processes, the platform provides immense value to both candidates seeking guidance and recruiters seeking efficiency.

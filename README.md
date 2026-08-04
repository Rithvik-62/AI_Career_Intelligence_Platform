# AI Career Intelligence Platform

![AI Career Intelligence Platform](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)

## Project Overview

The **AI Career Intelligence Platform** is an end-to-end, full-stack machine learning application designed to automate resume screening, predict career trajectories, and generate personalized learning roadmaps. It bridges the gap between raw candidate resumes and actionable career insights.

Built as an MCA Final Year Project, this platform demonstrates production-level software architecture, advanced Natural Language Processing (NLP) heuristics, and Machine Learning classification.

## Key Features

- **Intelligent Resume Parsing:** Extracts skills, experience, and education from PDFs with high accuracy.
- **AI Career Prediction:** Uses a Decision Tree model and TF-IDF vectorization to recommend optimal tech careers.
- **Skill Gap Analysis:** Compares your current skills against industry requirements to identify gaps.
- **Personalized Learning Roadmap:** Generates step-by-step learning paths for missing skills.
- **Dynamic Executive Dashboard:** Interactive Plotly charts and key performance indicators.
- **Professional PDF Export:** Download a beautifully formatted comprehensive Career Report via the Dashboard.
- **Live Job Matching:** Fetches real, active remote software engineering jobs based on your predicted role, with built-in offline fallbacks.
- **Presentation Demo Mode:** One-click instant population of a "Gold Standard" resume to seamlessly demonstrate the platform without uploading a file.

---

## Technology Stack

| Domain | Technology |
|---|---|
| **Language** | Python 3.9+ |
| **Frontend Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-Learn |
| **NLP & Text Extraction** | NLTK, pdfplumber, re |
| **Data Visualization** | Plotly Express, Plotly Graph Objects |
| **Export/Reporting** | ReportLab |

---

## Architecture & Data Flow

The platform follows a modular, decoupled architecture separating the presentation layer from the business logic.

1. **User Interface (`app/`)**: Handles file uploads and renders UI cards.
2. **Parser Service (`utils/parser.py`)**: Ingests PDF and outputs a structured JSON dictionary.
3. **ML Pipeline (`utils/predictor.py`)**: Cleans text, applies TF-IDF vectorization, and predicts the role using the cached `.pkl` model.
4. **Scoring Engine (`utils/scoring.py`)**: Uses the parsed dictionary to rate the resume structure out of 100.
5. **Gap Analyzer (`utils/skill_gap.py`)**: Cross-references parsed skills with the internal `CAREER_DATABASE`.

For deeper technical details, see [docs/architecture.md](docs/architecture.md).

---

## Folder Structure

```
AI_Career_Intelligence_Platform/
│
├── app/                        # Streamlit UI Layer
│   ├── streamlit_app.py        # Application entry point
│   ├── ui_components.py        # Centralized HTML/CSS rendering helpers
│   └── pages/                  # Streamlit multipage dashboard (Home, Prediction, Score, etc.)
│
├── config/                     # Centralized Configuration
│   └── settings.py             # App constants, paths, and skill mapping dicts
│
├── docs/                       # Technical Documentation
│   └── architecture.md         # System flow diagrams
│
├── logs/                       # Application Logs
│   └── app.log                 # Structured execution logs
│
├── models/                     # Serialized ML Artifacts (Git LFS or ignored)
│   ├── career_model.pkl        # Trained Decision Tree classifier
│   ├── label_encoder.pkl       # Target encoder
│   └── vectorizer.pkl          # TF-IDF vectorizer
│
├── scripts/                    # ML Pipeline scripts (EDA, Training, Validation)
├── tests/                      # Unit testing scripts for the parser and predictor
├── utils/                      # Core Business Logic (Parser, Predictor, Scorer, Roadmaps)
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-career-intelligence.git
   cd ai-career-intelligence
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure NLTK datasets are downloaded:**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

---

## How to Run

Launch the Streamlit dashboard by executing the entry point script from the root directory:

```bash
streamlit run app/streamlit_app.py
```

The application will be available at `http://localhost:8501`.

---

## Diagnostics & Troubleshooting

The platform includes built-in robustness checks to ensure a stable environment, specifically designed for university lab PC deployments where environments may vary.

### Environment Report
To generate a comprehensive health report of your environment, run:
```bash
python scripts/environment_report.py
```
This will test OS, Python version, dependencies, model presence, and folder permissions, providing PASS/FAIL/WARNING metrics.

### Automated Self-Test
To quickly verify all system requirements are met, run:
```bash
python scripts/self_test.py
```

### Common Errors & Recovery Steps

**Error:** `Python version 3.x is not supported.`
**Fix:** The application requires Python 3.11 or 3.12. Please upgrade or use the appropriate virtual environment.

**Error:** `Failed to import required packages.`
**Fix:** Ensure your virtual environment is active and run `pip install -r requirements.txt`.

**Error:** `Missing required model files.`
**Fix:** The ML models are missing from the `models/` directory. Run `python scripts/run_training.py` to regenerate the `career_model.pkl`, `vectorizer.pkl`, and `label_encoder.pkl`.

**Error:** `Missing NLTK resources.`
**Fix:** Run `python -m nltk.downloader punkt punkt_tab stopwords wordnet` to download required language data.

### 🎓 College Lab PC Deployment (Error-Free Setup)

If you are transferring this project to a restricted college computer (via USB or ZIP), you **MUST** follow these exact steps to prevent `DLL load failed`, NLTK resource missing, and AppLocker policy errors:

#### Step 1: Do NOT run it from the Pen Drive!
College PCs usually have strict security policies that block Python environments from running directly off USB drives (`E:\`, `F:\`).
1. Copy the entire `AI_Career_Intelligence_Platform` folder from your pen drive.
2. Paste it directly onto the College PC's **Desktop** (or Documents folder on the `C:\` drive). 

#### Step 2: Run the automated setup script
1. Open the folder you just copied to the Desktop.
2. Find the file named **`College_PC_Setup.bat`** and **double-click it**.

**What the script automatically does:**
- Safely deletes your home PC's `.venv` (preventing path mismatch errors).
- Creates a fresh Virtual Environment specifically for the college PC.
- Installs all dependencies from `requirements.txt`.
- Pre-downloads all `nltk` NLP resources (preventing download errors in the app).
- Automatically launches the Dashboard in your browser.

**Application Crash / Blank Page:**
Check the structured application logs located at `logs/app.log` for detailed Python tracebacks.

---

## Future Scope

- **LLM Integration**: Replace regex-based parsing with local LLMs (e.g., LLaMA 3) for higher extraction accuracy on unconventional resume formats.
- **Live Job Scraping**: Integrate with LinkedIn/Indeed APIs to recommend live job postings based on the predicted career.
- **Deep Learning Model**: Upgrade the Decision Tree classifier to a transformer-based sequence classifier (e.g., BERT) for semantic career matching.

---

## Author & License

**Developed for the Master of Computer Applications (MCA) Final Year Project.**

MIT License - free to use, modify, and distribute for educational and commercial purposes.

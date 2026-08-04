import sys
import os
import importlib
from config.settings import (
    MIN_PYTHON_VERSION, MAX_TESTED_PYTHON_VERSION,
    MODELS_DIR, DATASET_RAW_DIR, DATASET_PROCESSED_DIR, LOGS_DIR, TEMP_DIR,
    MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH,
    CLEAN_RESUME_DATASET, PREPROCESSED_RESUME_DATASET, RAW_RESUME_DATASET
)

def check_python_version():
    """Checks the Python version and returns a status dictionary."""
    current = sys.version_info[:2]
    if current < MIN_PYTHON_VERSION:
        return {
            "status": "FAIL",
            "message": f"Python version {current[0]}.{current[1]} is not supported. Minimum required is {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}.",
            "fix": "Please upgrade your Python installation."
        }
    if current > MAX_TESTED_PYTHON_VERSION:
        return {
            "status": "WARNING",
            "message": f"Python version {current[0]}.{current[1]} is newer than the maximum tested version {MAX_TESTED_PYTHON_VERSION[0]}.{MAX_TESTED_PYTHON_VERSION[1]}.",
            "fix": "The application may still work, but you might encounter unexpected issues."
        }
    return {"status": "PASS", "message": f"Python version {current[0]}.{current[1]} is supported."}


def check_directories():
    """Checks if required directories exist."""
    missing = []
    dirs = [MODELS_DIR, DATASET_RAW_DIR, DATASET_PROCESSED_DIR, LOGS_DIR, TEMP_DIR]
    for d in dirs:
        if not os.path.exists(d):
            missing.append(d)
        elif not os.access(d, os.W_OK | os.R_OK):
            missing.append(f"{d} (Permission Denied)")
            
    if missing:
        return {
            "status": "FAIL",
            "message": "Missing or inaccessible directories.",
            "details": missing,
            "fix": "Please ensure the directories exist and you have read/write permissions."
        }
    return {"status": "PASS", "message": "All required directories exist and are accessible."}


def check_models():
    """Checks if required model files exist."""
    missing = []
    models = [MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH]
    for m in models:
        if not os.path.exists(m):
            missing.append(m)
            
    if missing:
        return {
            "status": "FAIL",
            "message": "Missing required model files.",
            "details": missing,
            "fix": "Run 'python scripts/run_training.py' to generate the missing model files."
        }
    return {"status": "PASS", "message": "All required model files found."}


def check_datasets():
    """Checks if required dataset files exist."""
    missing = []
    datasets = [RAW_RESUME_DATASET] # Processed ones can be re-generated
    for d in datasets:
        if not os.path.exists(d):
            missing.append(d)
            
    if missing:
        return {
            "status": "FAIL",
            "message": "Missing raw dataset files.",
            "details": missing,
            "fix": "Please ensure 'Resume.csv' exists in 'dataset/raw/'."
        }
    return {"status": "PASS", "message": "Raw dataset files found."}


def check_packages():
    """Checks if required packages can be imported."""
    packages = [
        "numpy", "pandas", "sklearn", "matplotlib", 
        "joblib", "nltk", "streamlit", "pdfplumber", "plotly"
    ]
    failed = []
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError as e:
            failed.append({"package": pkg, "error": str(e)})
            
    if failed:
        details = [f"{f['package']}: {f['error']}" for f in failed]
        return {
            "status": "FAIL",
            "message": "Failed to import required packages.",
            "details": details,
            "fix": "Run 'pip install -r requirements.txt' to install missing packages. Check for virtual environment issues."
        }
    return {"status": "PASS", "message": "All required packages imported successfully."}

def check_nltk_resources():
    """Checks if required NLTK data is downloaded."""
    try:
        import nltk
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('tokenizers/punkt_tab')
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                nltk.data.find('corpora/wordnet.zip')
            return {"status": "PASS", "message": "Required NLTK resources found."}
        except LookupError:
            return {
                "status": "FAIL",
                "message": "Missing NLTK resources.",
                "fix": "Run 'python -m nltk.downloader punkt punkt_tab stopwords wordnet'"
            }
    except ImportError:
        return {"status": "FAIL", "message": "NLTK package not installed.", "fix": "pip install nltk"}


def run_all_diagnostics():
    """Runs all checks and returns a summary."""
    results = {
        "python": check_python_version(),
        "directories": check_directories(),
        "models": check_models(),
        "datasets": check_datasets(),
        "packages": check_packages(),
        "nltk": check_nltk_resources()
    }
    
    overall_status = "PASS"
    for k, v in results.items():
        if v["status"] == "FAIL":
            overall_status = "FAIL"
            break
        elif v["status"] == "WARNING" and overall_status == "PASS":
            overall_status = "WARNING"
            
    return {
        "overall_status": overall_status,
        "results": results
    }

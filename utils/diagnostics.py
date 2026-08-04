"""
System Environment Diagnostics
Validates the runtime environment before the application starts.
Cloud-aware: auto-repairs NLTK data and missing directories.
"""

import sys
import os
import importlib
from config.settings import (
    MIN_PYTHON_VERSION, MAX_TESTED_PYTHON_VERSION,
    MODELS_DIR, DATASET_RAW_DIR, DATASET_PROCESSED_DIR, LOGS_DIR, TEMP_DIR,
    MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH,
    RAW_RESUME_DATASET
)


def check_python_version():
    current = sys.version_info[:2]
    if current < MIN_PYTHON_VERSION:
        return {
            "status": "FAIL",
            "message": f"Python {current[0]}.{current[1]} is not supported. Minimum: {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}.",
            "fix": "Please upgrade your Python installation."
        }
    if current > MAX_TESTED_PYTHON_VERSION:
        return {
            "status": "WARNING",
            "message": f"Python {current[0]}.{current[1]} newer than max tested {MAX_TESTED_PYTHON_VERSION[0]}.{MAX_TESTED_PYTHON_VERSION[1]}.",
            "fix": "App may still work but could have edge-case issues."
        }
    return {"status": "PASS", "message": f"Python {current[0]}.{current[1]} supported."}


def check_directories():
    """Auto-creates missing directories instead of blocking startup."""
    for d in [MODELS_DIR, DATASET_RAW_DIR, DATASET_PROCESSED_DIR, LOGS_DIR, TEMP_DIR]:
        os.makedirs(d, exist_ok=True)
    return {"status": "PASS", "message": "All required directories verified/created."}


def check_models():
    """Checks if required ML model .pkl files exist."""
    missing = []
    for m in [MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH]:
        if not os.path.exists(m):
            missing.append(os.path.basename(m))

    if missing:
        return {
            "status": "FAIL",
            "message": f"Missing model files: {', '.join(missing)}",
            "details": missing,
            "fix": (
                "Trained model .pkl files are missing. On Streamlit Cloud this means the models/ folder "
                "was not committed to GitHub. Add models/*.pkl to git and push again."
            )
        }
    return {"status": "PASS", "message": "All ML model files found."}


def check_datasets():
    """Checks dataset — WARNING only (not required for live predictions)."""
    if not os.path.exists(RAW_RESUME_DATASET):
        return {
            "status": "WARNING",
            "message": "Raw dataset not found (Resume.csv). Dataset EDA page will be unavailable.",
            "fix": "Upload Resume.csv to dataset/raw/ for full EDA functionality."
        }
    return {"status": "PASS", "message": "Raw dataset found."}


def check_packages():
    packages = ["numpy", "pandas", "sklearn", "matplotlib", "joblib", "nltk", "streamlit", "pdfplumber", "plotly"]
    failed = []
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError as e:
            failed.append(f"{pkg}: {e}")

    if failed:
        return {
            "status": "FAIL",
            "message": "Failed to import required packages.",
            "details": failed,
            "fix": "Run 'pip install -r requirements.txt'"
        }
    return {"status": "PASS", "message": "All packages imported successfully."}


def check_nltk_resources():
    """Auto-downloads NLTK data if missing (handles cloud environment)."""
    try:
        import nltk

        # Set a writable download path for cloud environments
        nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
        os.makedirs(nltk_data_dir, exist_ok=True)
        if nltk_data_dir not in nltk.data.path:
            nltk.data.path.insert(0, nltk_data_dir)

        resources = [
            ("corpora/stopwords", "stopwords"),
            ("tokenizers/punkt_tab", "punkt_tab"),
            ("tokenizers/punkt", "punkt"),
            ("corpora/wordnet", "wordnet"),
        ]

        for find_path, download_id in resources:
            try:
                nltk.data.find(find_path)
            except LookupError:
                try:
                    nltk.download(download_id, quiet=True, download_dir=nltk_data_dir)
                except Exception:
                    pass  # Non-critical — app continues

        return {"status": "PASS", "message": "NLTK resources ready."}

    except ImportError:
        return {"status": "FAIL", "message": "NLTK not installed.", "fix": "pip install nltk"}


def run_all_diagnostics():
    """Runs all checks. Only FAIL on truly critical items (missing models or packages)."""
    results = {
        "python": check_python_version(),
        "directories": check_directories(),
        "models": check_models(),
        "datasets": check_datasets(),   # WARNING only — not a hard blocker
        "packages": check_packages(),
        "nltk": check_nltk_resources(),
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

"""
Career Prediction Engine (V2.0 Enhanced)
Responsible for orchestrating the parsing, cleaning, vectorization, multi-class prediction,
and feature contribution extraction for explainable AI.
"""

import os
import joblib
import sys
from typing import Dict, Any, List
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import MODELS_DIR
from utils.parser import ResumeParser
from utils.cleaner import clean_text
from utils.logger import app_logger

class CareerPredictor:
    """
    Inference and Explainable AI (XAI) service for career role classification.
    """
    def __init__(self, models_dir: str = MODELS_DIR):
        self.models_dir = models_dir
        self.parser = ResumeParser()
        
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        
        self._load_models()

    def _load_models(self):
        from config.settings import MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH
        try:
            if not all(os.path.exists(p) for p in [MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH]):
                raise FileNotFoundError("One or more model files are missing.")
                
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.label_encoder = joblib.load(LABEL_ENCODER_PATH)
            app_logger.info("ML Models loaded successfully.")
            
        except Exception as e:
            app_logger.error(f"Failed to load ML models: {str(e)}")
            self.model = None

    def _get_top_predictions(self, probabilities, top_n: int = 5) -> List[Dict[str, Any]]:
        """Extracts the Top N predicted roles, ranks, and confidence percentages."""
        top_indices = np.argsort(probabilities)[::-1][:top_n]
        top_preds = []
        
        for rank, idx in enumerate(top_indices, start=1):
            role_name = self.label_encoder.inverse_transform([idx])[0]
            confidence = round(float(probabilities[idx]) * 100, 2)
            top_preds.append({
                "rank": rank,
                "role": role_name,
                "confidence": confidence
            })
            
        return top_preds

    def extract_feature_contributions(self, cleaned_text: str, top_k: int = 8) -> List[Dict[str, Any]]:
        """
        Calculates feature importance by intersecting TF-IDF vocabulary weights
        for the given text instance.
        """
        if self.vectorizer is None:
            return []
            
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        vectorized = self.vectorizer.transform([cleaned_text]).toarray()[0]
        
        non_zero_indices = np.where(vectorized > 0)[0]
        if len(non_zero_indices) == 0:
            return []
            
        weights = vectorized[non_zero_indices]
        words = feature_names[non_zero_indices]
        
        # Sort by TF-IDF weight descending
        sorted_indices = np.argsort(weights)[::-1][:top_k]
        
        contributions = []
        for idx in sorted_indices:
            contributions.append({
                "feature": words[idx],
                "weight": round(float(weights[idx]), 4),
                "impact": "High" if weights[idx] > 0.2 else "Moderate"
            })
            
        return contributions

    def predict(self, pdf_file_path: str) -> Dict[str, Any]:
        if self.model is None or self.vectorizer is None or self.label_encoder is None:
            app_logger.error("Prediction attempted without loaded models.")
            return {"error": "Prediction service is unavailable due to missing models."}
            
        try:
            parsed_data = self.parser.parse(pdf_file_path)
            if "error" in parsed_data:
                return {"error": parsed_data["error"]}
                
            raw_text = self.parser._extract_text_from_pdf(pdf_file_path)
            if not raw_text.strip():
                return {"error": "Extracted text is empty. Cannot predict career."}

            cleaned_text = clean_text(raw_text)
            if not cleaned_text.strip():
                return {"error": "Text cleaning resulted in an empty string."}

            vectorized_text = self.vectorizer.transform([cleaned_text])
            feature_contributions = self.extract_feature_contributions(cleaned_text)
            
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(vectorized_text)[0]
                top_predictions = self._get_top_predictions(probabilities, top_n=5)
                top_role = top_predictions[0]["role"]
                top_conf = top_predictions[0]["confidence"]
                
                # Explanation string
                top_skills = [fc['feature'] for fc in feature_contributions[:3]]
                explanation_str = f"The model predicts '{top_role}' ({top_conf}% confidence) because your resume contains high TF-IDF feature weights for key terms: {', '.join(top_skills)}."
                
                return {
                    "predicted_role": top_role,
                    "confidence": top_conf,
                    "top_predictions": top_predictions,
                    "feature_contributions": feature_contributions,
                    "explanation": explanation_str,
                    "parsed_data": parsed_data
                }
            else:
                pred_idx = self.model.predict(vectorized_text)[0]
                pred_role = self.label_encoder.inverse_transform([pred_idx])[0]
                
                return {
                    "predicted_role": pred_role,
                    "confidence": 100.0,
                    "top_predictions": [{"rank": 1, "role": pred_role, "confidence": 100.0}],
                    "feature_contributions": feature_contributions,
                    "explanation": f"The model assigned '{pred_role}' based on decision tree classification rules.",
                    "parsed_data": parsed_data
                }
                
        except Exception as e:
            app_logger.error(f"Prediction pipeline failed: {str(e)}")
            return {"error": f"Prediction failed: {str(e)}"}

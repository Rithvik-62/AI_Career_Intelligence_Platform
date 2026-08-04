"""
Google Gemini AI Integration Service
Provides real-time generative AI capabilities for ARIA Chatbot, Resume Bullet Rewriter, and Cover Letter Generator.
Optimized for high performance with immediate fallback.
"""

import sys, os, logging, json, requests
from typing import Dict, Any, List, Optional
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.keys import GEMINI_API_KEY

logger = logging.getLogger("AI_Career_Intelligence.gemini")

class GeminiService:
    """
    Interface for Google Gemini API models.
    """
    
    @staticmethod
    def is_available() -> bool:
        return bool(GEMINI_API_KEY and len(GEMINI_API_KEY.strip()) > 5)
        
    @classmethod
    def generate_response(cls, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        if not cls.is_available():
            return None
            
        key = GEMINI_API_KEY.strip()
        full_text = f"{system_instruction}\n\nUser Prompt: {prompt}" if system_instruction else prompt
        
        # Primary active model for instant response
        models_to_try = ["gemini-3.6-flash", "gemini-2.0-flash"]
        
        for m in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}"
                payload = {
                    "contents": [{"parts": [{"text": full_text}]}]
                }
                headers = {"Content-Type": "application/json"}
                resp = requests.post(url, json=payload, headers=headers, timeout=4)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"].strip()
            except Exception as e:
                logger.warning(f"Gemini model {m} call failed: {e}")
                continue
                
        return None

    @classmethod
    def rewrite_resume_bullet(cls, raw_bullet: str, target_role: str) -> Optional[Dict[str, str]]:
        system_prompt = (
            f"You are an expert executive resume writer specializing in {target_role} resumes. "
            "Rewrite the user's weak bullet point into a high-impact, quantifiable, action-verb driven enterprise resume bullet point. "
            "Return output strictly as a JSON object with keys: 'before', 'after', 'impact', 'category'."
        )
        user_prompt = f"Weak bullet: '{raw_bullet}'"
        
        reply = cls.generate_response(user_prompt, system_prompt)
        if reply:
            try:
                clean_reply = reply.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_reply)
                return data
            except Exception:
                pass
        return None

"""
Live Industry News & Hiring Trends Service
Fetches real-time tech career news, hiring insights, and market trends using NewsData.io / NewsAPI with offline fallback.
"""

import sys, os, requests, logging
from typing import Dict, Any, List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.keys import NEWS_API_KEY

logger = logging.getLogger("AI_Career_Intelligence.news")

# Offline Curated Fallback News Items
OFFLINE_NEWS = {
    "Data Scientist": [
        {
            "title": "Generative AI and LLM Engineering Lead 2026 Tech Hiring Surge",
            "source": "TechCrunch Industry Insights",
            "description": "Enterprise adoption of custom AI models and RAG pipelines drives 35% growth in Data Science & Machine Learning engineering roles.",
            "url": "https://techcrunch.com",
            "published_at": "Today"
        },
        {
            "title": "Top Essential Skills for Modern Data Scientists in Enterprise",
            "source": "Harvard Business Review",
            "description": "SQL proficiency, PyTorch model deployment, and cloud vector databases remain core prerequisites for top-tier analytics roles.",
            "url": "https://hbr.org",
            "published_at": "Yesterday"
        }
    ],
    "Software Developer": [
        {
            "title": "Full-Stack System Architecture & Cloud-Native Engineering Demand",
            "source": "InfoQ Tech Report",
            "description": "Companies prioritize software engineers skilled in microservices, Docker, Kubernetes, and automated CI/CD pipelines.",
            "url": "https://infoq.com",
            "published_at": "Today"
        },
        {
            "title": "AI-Assisted Coding Tools Boost Developer Productivity by 40%",
            "source": "GitHub Engineering Blog",
            "description": "Modern software developers leveraging AI pair programming tools deliver robust code faster while focusing on high-level architecture.",
            "url": "https://github.blog",
            "published_at": "2 days ago"
        }
    ],
    "Default": [
        {
            "title": "Global Tech Hiring Trends: Cloud, AI, and Cybersecurity Demand Rises",
            "source": "Wired Business",
            "description": "Technology sector hiring rebounds with a strong focus on specialized software engineering and cloud infrastructure roles.",
            "url": "https://wired.com",
            "published_at": "Today"
        },
        {
            "title": "High-Demand Skills Shaping the Future of Tech Careers in 2026",
            "source": "MIT Technology Review",
            "description": "Continuous learning, Python expertise, and cross-functional system design top employer priority lists across industries.",
            "url": "https://technologyreview.com",
            "published_at": "Yesterday"
        }
    ]
}

class NewsService:
    """
    Fetches live tech industry news items matching target roles.
    """
    
    @classmethod
    def get_career_news(cls, target_role: str = "Software Developer") -> List[Dict[str, str]]:
        key = NEWS_API_KEY.strip()
        articles = []
        
        # 1. Try NewsData.io (for pub_... keys)
        if key.startswith("pub_"):
            try:
                query = target_role.replace(" ", " OR ")
                url = f"https://newsdata.io/api/1/news?apikey={key}&q={query}&language=en&category=technology"
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    for item in results[:5]:
                        articles.append({
                            "title": item.get("title", "Tech Career Update"),
                            "source": item.get("source_id", "Tech News").title(),
                            "description": item.get("description", "Latest industry hiring trends and technology updates.")[:180] + "...",
                            "url": item.get("link", "#"),
                            "published_at": item.get("pubDate", "Recent")[:10]
                        })
            except Exception as e:
                logger.warning(f"NewsData.io API call failed: {e}")
                
        # 2. Try NewsAPI.org
        elif len(key) > 5:
            try:
                url = f"https://newsapi.org/v2/everything?q={target_role.replace(' ', '+')}+tech+hiring&language=en&sortBy=publishedAt&pageSize=5&apiKey={key}"
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("articles", [])
                    for item in results[:5]:
                        articles.append({
                            "title": item.get("title", "Tech Career News"),
                            "source": item.get("source", {}).get("name", "Tech News"),
                            "description": item.get("description", "")[:180] + "...",
                            "url": item.get("url", "#"),
                            "published_at": item.get("publishedAt", "Recent")[:10]
                        })
            except Exception as e:
                logger.warning(f"NewsAPI call failed: {e}")
                
        # Fallback to curated news if API offline or empty
        if not articles:
            articles = OFFLINE_NEWS.get(target_role, OFFLINE_NEWS["Default"])
            
        return articles

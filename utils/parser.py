"""
Resume Parser Module V2.0 (Stabilized & Presentation-Ready)
Robust resume extraction engine supporting Microsoft Word, Canva, Overleaf (LaTeX),
Novoresume, Europass, ATS, and multi-page PDF templates.
"""

import pdfplumber
import re
import sys
import os
from typing import Dict, Any, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import SKILL_MAPPING
from utils.logger import app_logger

class ResumeParser:
    def __init__(self):
        # Comprehensive list of technical skills, frameworks, databases, cloud platforms & tools
        self.raw_skill_dict = [
            # Programming Languages
            "python", "java", "c", "c++", "cpp", "c#", "csharp", "javascript", "js", "typescript", "ts",
            "go", "golang", "rust", "r", "php", "ruby", "swift", "kotlin", "scala", "sql", "html", "css",
            "bash", "shell", "matlab", "dart",
            # Web Frameworks & Frontend/Backend
            "react", "react.js", "reactjs", "angular", "vue", "vue.js", "node.js", "nodejs", "express", "express.js",
            "spring boot", "spring", "django", "flask", "fastapi", "next.js", "nextjs", "bootstrap", "tailwind", "tailwind css",
            # AI / Data Science / ML
            "tensorflow", "pytorch", "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib", "seaborn",
            "opencv", "nltk", "spacy", "keras", "spark", "pyspark", "hadoop", "snowflake", "alteryx", "power bi", "tableau",
            # Databases
            "mysql", "postgresql", "postgres", "mongodb", "oracle", "sqlite", "redis", "cassandra", "dynamodb", "firebase",
            "sql server", "ms sql", "elasticsearch",
            # Cloud & DevOps
            "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "git", "github", "gitlab",
            "jenkins", "terraform", "ansible", "linux", "unix", "ci/cd", "cicd", "nginx", "apache",
            # Tools & Concepts
            "excel", "jira", "postman", "figma", "canva", "google analytics", "kafka", "rest api", "restful api",
            "microservices", "system design", "agile", "scrum", "machine learning", "deep learning", "computer vision",
            "nlp", "natural language processing", "mlops"
        ]

        # Normalization mapping from central config
        self.skill_normalization = SKILL_MAPPING

        # Words that CANNOT be part of a candidate's name
        self.non_name_words = set([
            "resume", "curriculum", "vitae", "cv", "page", "phone", "email", "mobile", "address",
            "location", "linkedin", "github", "portfolio", "summary", "objective", "profile",
            "education", "experience", "work", "projects", "skills", "certifications", "achievements",
            "engineer", "scientist", "developer", "analyst", "architect", "manager", "administrator",
            "intern", "consultant", "university", "college", "school", "institute", "technology",
            "department", "bachelor", "master", "phd", "degree", "diploma", "gpa", "present", "current",
            "january", "february", "march", "april", "may", "june", "july", "august", "september",
            "october", "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep",
            "oct", "nov", "dec", "towardsdatascience", "medium", "mobile"
        ])

        # Common US state codes & countries for high-precision location validation
        self.valid_regions = set([
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
            "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
            "VA", "WA", "WV", "WI", "WY", "DC", "India", "Pakistan", "Korea", "RepublicofKorea",
            "USA", "UK", "Canada", "Singapore", "Australia", "Germany", "France", "Japan"
        ])

    def _extract_text_from_pdf(self, file_path_or_bytes) -> str:
        """Extracts and cleans raw text from multi-page PDFs using pdfplumber."""
        text = ""
        try:
            with pdfplumber.open(file_path_or_bytes) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=2, y_tolerance=3)
                    if page_text:
                        text += page_text + "\n"
            
            # Clean invisible Unicode & PDF ligature artifacts
            text = text.replace('\xa0', ' ').replace('\xad', '').replace('\r', '\n')
            text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            if not text.strip():
                raise ValueError("Empty or scanned image PDF without extractable text.")
            return text
        except Exception as e:
            app_logger.error(f"Parser Error reading PDF: {str(e)}")
            raise ValueError(f"Corrupted or unsupported PDF file format: {str(e)}")

    def _extract_email(self, text: str) -> str:
        """Extracts and validates primary candidate email address."""
        match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
        return match.group(0).strip() if match else "Email Not Found"

    def _extract_phone(self, text: str) -> str:
        """Extracts and validates candidate phone number."""
        patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for m in matches:
                phone_candidate = m.group(0).strip()
                if not re.search(r'20\d{2}\s*-\s*20\d{2}', phone_candidate) and len(re.sub(r'\D', '', phone_candidate)) >= 7:
                    return phone_candidate
        return "Phone Not Found"

    def _extract_links(self, text: str) -> Dict[str, str]:
        """Extracts LinkedIn, GitHub, and Portfolio URLs."""
        links = {
            "linkedin": "LinkedIn Not Provided",
            "github": "GitHub Not Provided",
            "portfolio": "Portfolio Not Provided"
        }

        # LinkedIn Regex
        li_match = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?', text, re.IGNORECASE)
        if li_match:
            url = li_match.group(0).strip()
            links['linkedin'] = url if url.startswith('http') else 'https://' + url

        # GitHub Regex
        gh_match = re.search(r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?', text, re.IGNORECASE)
        if gh_match:
            url = gh_match.group(0).strip()
            links['github'] = url if url.startswith('http') else 'https://' + url

        # Portfolio Regex (other domain URLs like alexrivera.dev, sourabhbajaj.com)
        urls = re.findall(r'(?:https?://)?(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.(?:com|dev|io|org|net|me|in|co)(?:/[^\s]*)?', text)
        for url in urls:
            u_lower = url.lower()
            if not any(ignore in u_lower for ignore in ['linkedin.com', 'github.com', 'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'next.js']):
                links['portfolio'] = url if url.startswith('http') else 'https://' + url
                break

        return links

    def _extract_location(self, text: str) -> str:
        """Extracts candidate location (City, State / City, Country) with region validation."""
        lines = [l.strip() for l in text.split('\n')[:25] if l.strip()]
        
        for line in lines:
            match_state = re.search(r'\b([A-Z][a-zA-Z\s]{2,18}),\s*([A-Z]{2})\b', line)
            if match_state:
                city, region = match_state.group(1).strip(), match_state.group(2).strip()
                if region in self.valid_regions and city.lower() not in self.non_name_words:
                    return f"{city}, {region}"

            match_country = re.search(r'\b([A-Z][a-zA-Z\s]{2,18}),\s*([A-Z][a-zA-Z\s]{2,18})\b', line)
            if match_country:
                city, country = match_country.group(1).strip(), match_country.group(2).strip()
                if country in self.valid_regions and city.lower() not in self.non_name_words:
                    return f"{city}, {country}"

        return "Location Not Specified"

    def _extract_name(self, text: str) -> str:
        """
        High-Priority Candidate Name Extraction Engine.
        Searches top section of resume, strips URLs/emails/phones/titles, and scores candidate name tokens.
        """
        raw_lines = [line.strip() for line in text.split('\n')[:15] if line.strip()]
        
        for line in raw_lines:
            clean_line = re.sub(r'https?://[^\s]+', '', line, flags=re.IGNORECASE)
            clean_line = re.sub(r'(?:linkedin|github|towardsdatascience)\.com[^\s]*', '', clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '', clean_line)
            clean_line = re.sub(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '', clean_line)
            
            clean_line = re.sub(r'\b(Name|Curriculum Vitae|CV|Resume|Profile|Objective|Email|Mobile|Phone|Contact|MBA|Ph\.?D\.?|PMP|B\.?Tech|M\.?S\.?)\b', '', clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r'[^a-zA-Z\s.-]', '', clean_line).strip()
            
            if not clean_line:
                continue

            words = clean_line.split()
            valid_tokens = []
            
            for w in words:
                w_clean = w.strip('.-')
                if len(w_clean) < 2:
                    if len(w_clean) == 1 and w_clean.isalpha():
                        valid_tokens.append(w_clean.upper())
                    continue
                
                if w_clean.lower() in self.non_name_words:
                    break
                    
                if w_clean.isalpha():
                    valid_tokens.append(w_clean.title() if w_clean.islower() else w_clean)

            if 2 <= len(valid_tokens) <= 4:
                return " ".join(valid_tokens)
            elif len(valid_tokens) == 1 and len(words) == 1:
                return valid_tokens[0].title()

        return "Name Not Detected"

    def _extract_skills(self, text: str) -> List[str]:
        """Extracts and normalizes technical competencies using boundary-safe regex."""
        text_lower = text.lower()
        extracted_skills = set()

        for skill in self.raw_skill_dict:
            escaped_skill = re.escape(skill)
            if skill in ["c++", "cpp"]:
                pattern = r'(?<![\w])(c\+\+|cpp)(?![\w])'
            elif skill in ["c#", "csharp"]:
                pattern = r'(?<![\w])(c\#|csharp)(?![\w])'
            elif skill in ["r"]:
                pattern = r'\b(r)\b'
            elif skill in ["go", "golang"]:
                pattern = r'\b(go|golang)\b'
            else:
                pattern = r'(?<![\w])' + escaped_skill + r'(?![\w])'

            if re.search(pattern, text_lower):
                normalized = self.skill_normalization.get(skill, skill.title() if len(skill) > 3 else skill.upper())
                extracted_skills.add(normalized)

        for variation, normalized in self.skill_normalization.items():
            pattern = r'(?<![\w])' + re.escape(variation) + r'(?![\w])'
            if re.search(pattern, text_lower):
                extracted_skills.add(normalized)

        return sorted(list(extracted_skills))

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extracts raw text blocks for key resume sections."""
        sections = {
            "education": "", "experience": "", "projects": "",
            "certifications": "", "achievements": "", "publications": "",
            "summary": ""
        }

        current_section = None
        lines = text.split('\n')

        for line in lines:
            line_clean = line.strip().lower()
            
            if re.match(r'^(\d+\.\s*)?(education|academic background|academic details|qualification|education & training)[^a-z]*$', line_clean):
                current_section = 'education'
                continue
            elif re.match(r'^(\d+\.\s*)?(experience|work experience|employment history|professional experience|career history|internships)[^a-z]*$', line_clean):
                current_section = 'experience'
                continue
            elif re.match(r'^(\d+\.\s*)?(projects|academic projects|personal projects|key projects|software projects)[^a-z]*$', line_clean):
                current_section = 'projects'
                continue
            elif re.match(r'^(\d+\.\s*)?(certifications|courses|licenses|certifications & licenses|courses & certifications)[^a-z]*$', line_clean):
                current_section = 'certifications'
                continue
            elif re.match(r'^(\d+\.\s*)?(achievements|awards|honors|accomplishments|hackathons|competitions)[^a-z]*$', line_clean):
                current_section = 'achievements'
                continue
            elif re.match(r'^(\d+\.\s*)?(publications|patents|research papers)[^a-z]*$', line_clean):
                current_section = 'publications'
                continue
            elif re.match(r'^(\d+\.\s*)?(summary|profile|professional summary|executive summary|about me|objective)[^a-z]*$', line_clean):
                current_section = 'summary'
                continue
            elif re.match(r'^(\d+\.\s*)?(skills|technical skills|core competencies|skills & tools|tech stack|reasoning skills|languages)[^a-z]*$', line_clean):
                current_section = None
                continue

            if current_section and line.strip():
                sections[current_section] += line.strip() + "\n"

        return sections

    def _parse_experience(self, text: str) -> List[Dict[str, Any]]:
        """Parses experience text into structured job entry blocks."""
        if not text.strip():
            return []

        date_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|20\d{2})\s*(?:-|to)\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|20\d{2}|Present|Current)'
        
        chunks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
        if not chunks:
            chunks = [text.strip()]

        parsed_blocks = []
        for chunk in chunks:
            lines = chunk.strip().split('\n')
            dates = re.search(date_pattern, chunk, re.IGNORECASE)
            date_str = dates.group(0) if dates else "Dates Not Specified"

            title = lines[0] if lines else "Role Not Specified"
            company = lines[1] if len(lines) > 1 and not re.search(date_pattern, lines[1], re.IGNORECASE) else "Company Not Specified"

            parsed_blocks.append({
                "job_title": title,
                "company": company,
                "dates": date_str,
                "description": chunk
            })
        return parsed_blocks

    def _parse_projects(self, text: str) -> List[Dict[str, Any]]:
        """Parses project text into structured project entry blocks."""
        if not text.strip():
            return []

        chunks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
        if not chunks:
            chunks = [text.strip()]

        parsed_blocks = []
        for chunk in chunks:
            lines = chunk.strip().split('\n')
            title = lines[0] if lines else "Project Title Not Specified"
            techs = self._extract_skills(chunk)

            parsed_blocks.append({
                "project_title": title,
                "technologies": techs,
                "description": chunk
            })
        return parsed_blocks

    def _parse_education(self, text: str) -> List[Dict[str, Any]]:
        """Parses education text into structured degree entry blocks."""
        if not text.strip():
            return []

        chunks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
        if not chunks:
            chunks = [text.strip()]

        parsed_blocks = []
        for chunk in chunks:
            lines = chunk.strip().split('\n')
            degree = lines[0] if lines else "Degree Not Specified"

            parsed_blocks.append({
                "degree": degree,
                "university": "Institution details contained in description",
                "description": chunk
            })
        return parsed_blocks

    def _parse_certifications(self, text: str) -> List[Dict[str, Any]]:
        """Parses certifications and courses into structured title & description entries."""
        if not text.strip():
            return []

        blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
        if not blocks:
            blocks = [text.strip()]

        parsed_certs = []
        for block in blocks:
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            if not lines:
                continue

            # Determine title line (first line without bullet symbol if available)
            title_line = lines[0]
            for l in lines:
                if not l.startswith(('•', '-', '*', '', '')):
                    title_line = l
                    break

            desc_lines = [l for l in lines if l != title_line]
            desc_str = " ".join([re.sub(r'^[•\-\*]\s*', '', l) for l in desc_lines])

            parsed_certs.append({
                "title": re.sub(r'^[•\-\*]\s*', '', title_line),
                "description": desc_str
            })

        return parsed_certs

    def _parse_list_section(self, text: str) -> List[str]:
        """Parses list sections into cleaned bullet point items."""
        if not text.strip():
            return []

        text = re.sub(r'^[ \t]*[-*•][ \t]+', '• ', text, flags=re.MULTILINE)
        if '•' in text:
            items = re.split(r'\n(?=•)', text)
            return [item.replace('•', '').replace('\n', ' ').strip() for item in items if item.strip()]

        chunks = re.split(r'\n\s*\n', text.strip())
        if len(chunks) > 1:
            return [chunk.replace('\n', ' ').strip() for chunk in chunks if chunk.strip()]

        return [line.strip() for line in text.split('\n') if line.strip()]

    def parse(self, file_path_or_bytes) -> Dict[str, Any]:
        """
        Main Parsing Pipeline.
        Extracts candidate contact info, skills, sections, and returns structured metadata.
        Fault-tolerant: never crashes and returns safe fallbacks for missing fields.
        """
        app_logger.info("Starting resume extraction...")
        try:
            text = self._extract_text_from_pdf(file_path_or_bytes)
        except Exception as e:
            app_logger.error(f"Parser exception: {str(e)}")
            return {
                "name": "Name Not Detected",
                "email": "Email Not Found",
                "phone": "Phone Not Found",
                "location": "Location Not Specified",
                "linkedin": "LinkedIn Not Provided",
                "github": "GitHub Not Provided",
                "portfolio": "Portfolio Not Provided",
                "skills": [],
                "education": [],
                "experience": [],
                "projects": [],
                "certifications": [],
                "achievements": [],
                "publications": [],
                "metadata": {"parsing_confidence": 0.0},
                "error": str(e)
            }

        links = self._extract_links(text)
        sections_raw = self._extract_sections(text)

        extracted_data = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "location": self._extract_location(text),
            "linkedin": links.get('linkedin', 'LinkedIn Not Provided'),
            "github": links.get('github', 'GitHub Not Provided'),
            "portfolio": links.get('portfolio', 'Portfolio Not Provided'),
            "skills": self._extract_skills(text),
            "education": self._parse_education(sections_raw.get('education', '')),
            "experience": self._parse_experience(sections_raw.get('experience', '')),
            "projects": self._parse_projects(sections_raw.get('projects', '')),
            "certifications": self._parse_certifications(sections_raw.get('certifications', '')),
            "achievements": self._parse_list_section(sections_raw.get('achievements', '')),
            "publications": self._parse_list_section(sections_raw.get('publications', '')),
            "metadata": {
                "parsing_confidence": 0.0
            }
        }

        # Calculate parsing confidence score
        score = 0
        if extracted_data["name"] != "Name Not Detected": score += 20
        if extracted_data["email"] != "Email Not Found": score += 20
        if extracted_data["phone"] != "Phone Not Found": score += 15
        if extracted_data["skills"]: score += 20
        if extracted_data["experience"] or extracted_data["projects"]: score += 15
        if extracted_data["education"]: score += 10

        extracted_data["metadata"]["parsing_confidence"] = min(100.0, float(score))

        app_logger.info("Extraction completed successfully.")
        return extracted_data

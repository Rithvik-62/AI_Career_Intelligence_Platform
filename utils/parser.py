"""
Resume Parser Module
Responsible for extracting structured data from PDF resumes using regex and keyword heuristics.
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
        # Comprehensive list of skills
        self.raw_skill_dict = [
            "python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "rust", "r", "sql", "html", "css",
            "react", "angular", "vue", "node.js", "spring boot", "django", "flask", 
            "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "opencv",
            "mysql", "postgresql", "mongodb", "oracle", "sqlite",
            "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "jenkins", "terraform",
            "power bi", "tableau", "excel", "spark", "hadoop", "snowflake", "alteryx"
        ]
        
        # Normalization mapping from central config
        self.skill_normalization = SKILL_MAPPING

    def _extract_text_from_pdf(self, file_path_or_bytes) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path_or_bytes) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=2, y_tolerance=3)
                    if page_text:
                        text += page_text + "\n"
            if not text.strip():
                raise ValueError("Empty PDF or Image-based PDF without OCR.")
            return text
        except Exception as e:
            app_logger.error(f"Parser Error: Corrupted or unsupported file format: {str(e)}")
            raise ValueError(f"Corrupted or unsupported file format: {str(e)}")

    def _extract_email(self, text: str) -> Optional[str]:
        match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        match = re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return match.group(0).strip() if match else None

    def _extract_links(self, text: str) -> Dict[str, Optional[str]]:
        links = {"linkedin": None, "github": None, "portfolio": None}
        
        linkedin_match = re.search(r'(https?://(?:www\.)?linkedin\.com/(?:in|profile)/[^\s]+)', text, re.IGNORECASE)
        if linkedin_match: links['linkedin'] = linkedin_match.group(0)
            
        github_match = re.search(r'(https?://(?:www\.)?github\.com/[^\s]+)', text, re.IGNORECASE)
        if github_match: links['github'] = github_match.group(0)
        
        # Portfolio: any other valid http link that isn't linkedin or github
        urls = re.findall(r'(https?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s]*)', text)
        for url in urls:
            if "linkedin.com" not in url.lower() and "github.com" not in url.lower():
                links['portfolio'] = url
                break
                
        return links

    def _extract_location(self, text: str) -> Optional[str]:
        # Simple heuristic: look for City, State/Country near the top
        lines = text.split('\n')[:15]
        for line in lines:
            match = re.search(r'\b([A-Z][a-zA-Z\s]+),\s*([A-Z]{2}|[A-Z][a-zA-Z\s]+)\b', line)
            if match and len(match.group(1)) > 2:
                return match.group(0)
        return None

    def _extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        extracted_skills = set()
        
        for skill in self.raw_skill_dict:
            # Special regex to handle C++, C#, Node.js properly without standard \b issues
            escaped_skill = re.escape(skill)
            pattern = r'(?<![\w])' + escaped_skill + r'(?![\w])'
            if re.search(pattern, text_lower):
                normalized = self.skill_normalization.get(skill, skill.title() if len(skill)>2 else skill.upper())
                extracted_skills.add(normalized)
                
        # Also check common variations
        for variation, normalized in self.skill_normalization.items():
            pattern = r'(?<![\w])' + re.escape(variation) + r'(?![\w])'
            if re.search(pattern, text_lower):
                extracted_skills.add(normalized)
                
        return sorted(list(extracted_skills))

    def _extract_name(self, text: str) -> Optional[str]:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:5]:
            # Ignore lines that look like contact info
            if '@' in line or re.search(r'\d{5}', line) or 'github' in line.lower() or 'linkedin' in line.lower():
                continue
            name = re.sub(r'[^a-zA-Z\s.-]', '', line).strip()
            if len(name.split()) >= 1 and len(name) > 2:
                return name
        return None

    def _extract_sections(self, text: str) -> Dict[str, str]:
        sections = {
            "education": "", "experience": "", "projects": "", 
            "certifications": "", "achievements": "", "publications": ""
        }
        
        current_section = None
        lines = text.split('\n')
        
        for line in lines:
            line_clean = line.strip().lower()
            
            # Regex for headers to handle "WORK EXPERIENCE :" etc.
            if re.match(r'^(education|academic background|academic history|education details)[^a-z]*$', line_clean):
                current_section = 'education'
                continue
            elif re.match(r'^(experience|work experience|employment history|professional experience|career history)[^a-z]*$', line_clean):
                current_section = 'experience'
                continue
            elif re.match(r'^(projects|academic projects|personal projects)[^a-z]*$', line_clean):
                current_section = 'projects'
                continue
            elif re.match(r'^(certifications|licenses|courses)[^a-z]*$', line_clean):
                current_section = 'certifications'
                continue
            elif re.match(r'^(achievements|awards|honors|competitions|hackathons)[^a-z]*$', line_clean):
                current_section = 'achievements'
                continue
            elif re.match(r'^(publications|patents)[^a-z]*$', line_clean):
                current_section = 'publications'
                continue
            elif re.match(r'^(skills|technical skills|core competencies|summary|profile|objective)[^a-z]*$', line_clean):
                current_section = None
                continue
                
            if current_section and line.strip():
                sections[current_section] += line.strip() + "\n"
                
        return sections

    def _parse_experience(self, text: str) -> List[Dict[str, Any]]:
        blocks = []
        if not text.strip(): return blocks
        
        # Split by typical date patterns acting as new job markers
        date_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|20\d{2})\s*(?:-|to)\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|20\d{2}|Present|Current)'
        
        # Try splitting by double newline first, if it exists
        chunks = re.split(r'\n\s*\n', text.strip())
        if len(chunks) == 1:
            # Fallback to date split
            lines = text.split('\n')
            current_block = []
            for line in lines:
                if re.search(date_pattern, line, re.IGNORECASE) and current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)
            if current_block:
                blocks.append('\n'.join(current_block))
        else:
            blocks = chunks

        parsed_blocks = []
        for block in blocks:
            if not block.strip(): continue
            dates = re.search(date_pattern, block, re.IGNORECASE)
            date_str = dates.group(0) if dates else "Unknown Dates"
            
            lines = block.strip().split('\n')
            title = lines[0] if lines else "Unknown Role"
            company = lines[1] if len(lines) > 1 and not re.search(date_pattern, lines[1], re.IGNORECASE) else "Unknown Company"
            
            parsed_blocks.append({
                "job_title": title,
                "company": company,
                "dates": date_str,
                "description": block
            })
        return parsed_blocks

    def _parse_projects(self, text: str) -> List[Dict[str, Any]]:
        blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
        if not blocks:
            # If no blank lines, treat whole block as 1 project
            blocks = [text.strip()] if text.strip() else []
            
        parsed_blocks = []
        for block in blocks:
            lines = block.strip().split('\n')
            title = lines[0] if lines else "Unknown Project"
            
            # Simple tech extraction inside project
            techs = self._extract_skills(block)
            
            parsed_blocks.append({
                "project_title": title,
                "technologies": techs,
                "description": block
            })
        return parsed_blocks

    def _parse_education(self, text: str) -> List[Dict[str, Any]]:
        blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
        if not blocks:
            blocks = [text.strip()] if text.strip() else []
            
        parsed_blocks = []
        for block in blocks:
            lines = block.strip().split('\n')
            degree = lines[0] if lines else "Unknown Degree"
            
            parsed_blocks.append({
                "degree": degree,
                "university": "University/College details in description",
                "description": block
            })
        return parsed_blocks
        
    def _parse_list_section(self, text: str) -> List[str]:
        if not text.strip(): return []
        
        # Normalize various bullet points
        text = re.sub(r'^[ \t]*[-*][ \t]+', '• ', text, flags=re.MULTILINE)
        
        # Split by explicit bullet points if present
        if '•' in text:
            items = re.split(r'\n(?=•)', text)
            return [item.replace('\n', ' ').strip() for item in items if item.strip()]
            
        # Split by double newline to preserve multiline strings
        blocks = re.split(r'\n\s*\n', text.strip())
        if len(blocks) > 1:
            return [block.replace('\n', ' ').strip() for block in blocks if block.strip()]
            
        # Fallback to single newlines only if no other structure exists
        return [line.strip() for line in text.split('\n') if line.strip()]

    def parse(self, file_path_or_bytes) -> Dict[str, Any]:
        app_logger.info("Starting resume extraction...")
        try:
            text = self._extract_text_from_pdf(file_path_or_bytes)
        except Exception as e:
            app_logger.error(f"Parser exception: {str(e)}")
            return {"error": str(e)}

        links = self._extract_links(text)
        sections_raw = self._extract_sections(text)
        
        extracted_data = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "location": self._extract_location(text),
            "linkedin": links.get('linkedin'),
            "github": links.get('github'),
            "portfolio": links.get('portfolio'),
            "skills": self._extract_skills(text),
            "education": self._parse_education(sections_raw.get('education', '')),
            "experience": self._parse_experience(sections_raw.get('experience', '')),
            "projects": self._parse_projects(sections_raw.get('projects', '')),
            "certifications": self._parse_list_section(sections_raw.get('certifications', '')),
            "achievements": self._parse_list_section(sections_raw.get('achievements', '')),
            "publications": self._parse_list_section(sections_raw.get('publications', '')),
            "metadata": {
                "parsing_confidence": 0.0 # Will calculate below
            }
        }
        
        # Basic confidence score heuristic
        score = 0
        if extracted_data["name"]: score += 15
        if extracted_data["email"]: score += 15
        if extracted_data["phone"]: score += 10
        if extracted_data["skills"]: score += 20
        if extracted_data["experience"]: score += 20
        if extracted_data["education"]: score += 20
        
        extracted_data["metadata"]["parsing_confidence"] = min(100.0, float(score))
        
        app_logger.info("Extraction complete successfully.")
        return extracted_data

import os
import re
import PyPDF2
import docx
from typing import Dict, List, Any

class ResumeParser:
    def __init__(self):
        # Define common section headers
        self.section_headers = {
            'education': ["education", "academic background", "qualifications", "academic"],
            'experience': ["experience", "work experience", "employment history", "professional experience", "work history"],
            'skills': ["skills", "technical skills", "core competencies", "competencies", "abilities"]
        }
    

    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume file and extract relevant information.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Dictionary containing parsed resume data
        """
        # Extract text from file based on file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            text = self._extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            text = self._extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self._extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Process the extracted text
        return self._process_text(text)
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
        return text
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting text from DOCX: {str(e)}")
        return text
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with a different encoding if utf-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            print(f"Error extracting text from TXT: {str(e)}")
            return ""
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """
        Process the extracted text to identify and extract relevant information.
        
        Args:
            text: Extracted text from resume
            
        Returns:
            Dictionary containing parsed resume data
        """
        # Initialize result dictionary
        result = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": self._extract_skills(text),
            "education": self._extract_education(text),
            "experience": self._extract_experience(text)
        }
        
        return result
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name from the document."""
        # Simple heuristic: First 5 lines might contain the name
        first_lines = "\n".join(text.split("\n")[:5])
        
        # Look for patterns that might indicate a name (e.g., capitalized words)
        name_pattern = r'([A-Z][a-z]+ [A-Z][a-z]+)'
        matches = re.findall(name_pattern, first_lines)
        
        if matches:
            # Return the first match that's not a common header
            common_headers = ["resume", "curriculum vitae", "cv", "profile"]
            for match in matches:
                if match.lower() not in common_headers:
                    return match
        
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from the document."""
        # Use regex to find email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        if emails:
            return emails[0]
        
        return ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from the document."""
        # Use regex to find phone numbers
        phone_pattern = r'(\+\d{1,3}[-\.\s]?)?(\(?\d{3}\)?[-\.\s]?)?(\d{3}[-\.\s]?\d{4})'
        phones = re.findall(phone_pattern, text)
        
        if phones:
            # Join the matched groups and clean up
            phone = ''.join(''.join(tup) for tup in phones[0])
            return phone
        
        return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from the document."""
        # Common technical skills to look for
        common_skills = [
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin",
            "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "spring",
            "sql", "mysql", "postgresql", "mongodb", "oracle", "nosql", "aws", "azure", "gcp",
            "docker", "kubernetes", "jenkins", "git", "jira", "agile", "scrum", "devops",
            "machine learning", "artificial intelligence", "data science", "big data", "hadoop",
            "spark", "tensorflow", "pytorch", "nlp", "computer vision", "data analysis",
            "tableau", "power bi", "excel", "word", "powerpoint", "photoshop", "illustrator",
            "figma", "ui/ux", "project management", "leadership", "communication"
        ]
        
        # Find skills section
        skills_section = self._find_section(text, self.section_headers['skills'])
        
        # If skills section found, extract skills from there
        if skills_section:
            # Look for bullet points or comma-separated lists
            if "•" in skills_section:
                skills = [s.strip() for s in skills_section.split("•") if s.strip()]
            elif "," in skills_section:
                skills = [s.strip() for s in skills_section.split(",") if s.strip()]
            else:
                # Split by newlines and filter empty strings
                skills = [s.strip() for s in skills_section.split("\n") if s.strip()]
            
            # Remove any skills that are too long (likely not a skill)
            skills = [s for s in skills if len(s) < 50]
            
            return skills[:20]  # Limit to 20 skills
        
        # If no skills section found, look for common skills in the entire text
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
                found_skills.append(skill)
        
        return found_skills[:20]  # Limit to 20 skills
    
    def _extract_education(self, text: str) -> str:
        """Extract education information from the document."""
        # Find education section
        education_section = self._find_section(text, self.section_headers['education'])
        
        if education_section:
            # Limit to a reasonable length
            return education_section[:500]
        
        return ""
    
    def _extract_experience(self, text: str) -> str:
        """Extract work experience information from the document."""
        # Find experience section
        experience_section = self._find_section(text, self.section_headers['experience'])
        
        if experience_section:
            # Limit to a reasonable length
            return experience_section[:1000]
        
        return ""
    
    def _find_section(self, text: str, section_headers: List[str]) -> str:
        """
        Find a specific section in the resume text.
        
        Args:
            text: The resume text
            section_headers: List of possible section headers
            
        Returns:
            The text of the section if found, empty string otherwise
        """
        # Split text into lines
        lines = text.split("\n")
        
        # Find the start of the section
        start_idx = -1
        for i, line in enumerate(lines):
            for header in section_headers:
                if re.search(r'\b' + re.escape(header) + r'\b', line.lower()):
                    start_idx = i
                    break
            if start_idx != -1:
                break
        
        if start_idx == -1:
            return ""
        
        # Find the end of the section (next section header or end of document)
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            # Common section headers that might indicate the end of the current section
            if re.search(r'\b(education|experience|skills|projects|certifications|references|contact|about|summary|objective)\b', lines[i].lower()):
                # Check if this is not a continuation of the current section
                if not any(header in lines[i].lower() for header in section_headers):
                    end_idx = i
                    break
        
        # Extract the section text
        section_text = "\n".join(lines[start_idx:end_idx]).strip()
        
        return section_text

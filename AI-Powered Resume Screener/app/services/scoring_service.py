from typing import Dict, Any, List, Tuple
import re

class ScoringService:
    """
    Service for calculating match scores between resumes and job descriptions.
    """
    
    def __init__(self):
        """Initialize the scoring service."""
        # Define weights for different matching criteria
        self.weights = {
            'skills': 0.5,
            'experience': 0.3,
            'education': 0.2
        }
    
    def calculate_match_score(self, resume_features: Dict[str, Any], job_features: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate a match score between a resume and a job.
        
        Args:
            resume_features: Dictionary containing processed resume features
            job_features: Dictionary containing processed job features
            
        Returns:
            Tuple containing:
                - match_score: A float between 0 and 100 representing the match percentage
                - match_details: Dictionary with detailed scoring information
        """
        # Initialize scores
        skill_score = self._calculate_skill_match(resume_features.get('skills', []), 
                                                job_features.get('required_skills', []))
        
        experience_score = self._calculate_experience_match(resume_features.get('experience', ''), 
                                                          job_features.get('required_experience', ''))
        
        education_score = self._calculate_education_match(resume_features.get('education', ''), 
                                                        job_features.get('required_education', ''))
        
        # Calculate weighted score
        weighted_score = (
            skill_score * self.weights['skills'] +
            experience_score * self.weights['experience'] +
            education_score * self.weights['education']
        )
        
        # Convert to percentage
        match_score = round(weighted_score * 100, 1)
        
        # Prepare detailed match information
        match_details = {
            'skill_score': round(skill_score * 100, 1),
            'experience_score': round(experience_score * 100, 1),
            'education_score': round(education_score * 100, 1),
            'matching_skills': self._get_matching_skills(resume_features.get('skills', []), 
                                                      job_features.get('required_skills', [])),
            'missing_skills': self._get_missing_skills(resume_features.get('skills', []), 
                                                    job_features.get('required_skills', []))
        }
        
        return match_score, match_details
    
    def _calculate_skill_match(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """
        Calculate the skill match score.
        
        Args:
            resume_skills: List of skills from the resume
            job_skills: List of required skills from the job
            
        Returns:
            A float between 0 and 1 representing the skill match score
        """
        if not job_skills:
            return 1.0  # If no skills required, perfect match
        
        # Normalize skills (lowercase and strip)
        resume_skills_norm = [s.lower().strip() for s in resume_skills]
        job_skills_norm = [s.lower().strip() for s in job_skills]
        
        # Count matching skills
        matching_skills = sum(1 for skill in job_skills_norm if any(
            self._is_skill_match(skill, resume_skill) for resume_skill in resume_skills_norm
        ))
        
        # Calculate score
        return matching_skills / len(job_skills) if job_skills else 0
    
    def _is_skill_match(self, job_skill: str, resume_skill: str) -> bool:
        """
        Check if a resume skill matches a job skill, accounting for variations.
        
        Args:
            job_skill: A required skill from the job
            resume_skill: A skill from the resume
            
        Returns:
            Boolean indicating if the skills match
        """
        # Exact match
        if job_skill == resume_skill:
            return True
        
        # Check if one contains the other
        if job_skill in resume_skill or resume_skill in job_skill:
            return True
        
        # Check for common abbreviations and variations
        # For example, "JavaScript" and "JS" or "React.js" and "React"
        common_variations = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'react': 'reactjs',
            'node': 'nodejs',
            'vue': 'vuejs',
            'ml': 'machine learning',
            'ai': 'artificial intelligence',
            'ui': 'user interface',
            'ux': 'user experience'
        }
        
        # Check if the skills match after accounting for variations
        job_skill_lower = job_skill.lower()
        resume_skill_lower = resume_skill.lower()
        
        for abbr, full in common_variations.items():
            if (job_skill_lower == abbr and full in resume_skill_lower) or \
               (resume_skill_lower == abbr and full in job_skill_lower):
                return True
        
        return False
    
    def _calculate_experience_match(self, resume_experience: str, required_experience: str) -> float:
        """
        Calculate the experience match score.
        
        Args:
            resume_experience: Experience section from the resume
            required_experience: Required experience from the job
            
        Returns:
            A float between 0 and 1 representing the experience match score
        """
        if not required_experience:
            return 1.0  # If no experience required, perfect match
        
        # Extract years of experience from both strings
        resume_years = self._extract_years_of_experience(resume_experience)
        required_years = self._extract_years_of_experience(required_experience)
        
        if required_years == 0:
            return 1.0  # If no specific years required, assume match
        
        if resume_years == 0:
            return 0.0  # If no years found in resume, no match
        
        # Calculate score based on years
        if resume_years >= required_years:
            return 1.0  # Full match if resume has more experience than required
        else:
            # Partial match based on percentage of required years
            return resume_years / required_years
    
    def _extract_years_of_experience(self, text: str) -> int:
        """
        Extract the number of years of experience from text.
        
        Args:
            text: Text containing experience information
            
        Returns:
            Integer representing the number of years of experience
        """
        # Look for patterns like "X years" or "X+ years"
        year_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs',
            r'(\d+)\+?\s*yr',
            r'(\d+)\+?\s*y\.?o\.?e',
            r'(\d+)\+?\s*year\s*experience'
        ]
        
        for pattern in year_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Return the highest number of years found
                return max(int(match) for match in matches)
        
        return 0  # Default if no years found
    
    def _calculate_education_match(self, resume_education: str, required_education: str) -> float:
        """
        Calculate the education match score.
        
        Args:
            resume_education: Education section from the resume
            required_education: Required education from the job
            
        Returns:
            A float between 0 and 1 representing the education match score
        """
        if not required_education:
            return 1.0  # If no education required, perfect match
        
        # Define education levels and their corresponding values
        education_levels = {
            'high school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5,
            'doctorate': 5
        }
        
        # Extract education level from both strings
        resume_level = self._extract_education_level(resume_education, education_levels)
        required_level = self._extract_education_level(required_education, education_levels)
        
        if required_level == 0:
            return 1.0  # If no specific level required, assume match
        
        if resume_level == 0:
            return 0.0  # If no level found in resume, no match
        
        # Calculate score based on education level
        if resume_level >= required_level:
            return 1.0  # Full match if resume has higher or equal education
        else:
            # Partial match based on percentage of required level
            return resume_level / required_level
    
    def _extract_education_level(self, text: str, education_levels: Dict[str, int]) -> int:
        """
        Extract the education level from text.
        
        Args:
            text: Text containing education information
            education_levels: Dictionary mapping education level terms to numeric values
            
        Returns:
            Integer representing the education level
        """
        # Find the highest education level mentioned
        max_level = 0
        
        for level, value in education_levels.items():
            if re.search(r'\b' + re.escape(level) + r'\b', text.lower()):
                max_level = max(max_level, value)
        
        return max_level
    
    def _get_matching_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """
        Get a list of skills that match between the resume and job.
        
        Args:
            resume_skills: List of skills from the resume
            job_skills: List of required skills from the job
            
        Returns:
            List of matching skills
        """
        # Normalize skills
        resume_skills_norm = [s.lower().strip() for s in resume_skills]
        job_skills_norm = [s.lower().strip() for s in job_skills]
        
        # Find matching skills
        matching = []
        for job_skill in job_skills_norm:
            for resume_skill in resume_skills_norm:
                if self._is_skill_match(job_skill, resume_skill):
                    # Use the job skill name for consistency
                    matching.append(job_skill)
                    break
        
        return matching
    
    def _get_missing_skills(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """
        Get a list of required skills that are missing from the resume.
        
        Args:
            resume_skills: List of skills from the resume
            job_skills: List of required skills from the job
            
        Returns:
            List of missing skills
        """
        # Normalize skills
        resume_skills_norm = [s.lower().strip() for s in resume_skills]
        job_skills_norm = [s.lower().strip() for s in job_skills]
        
        # Find missing skills
        missing = []
        for job_skill in job_skills_norm:
            if not any(self._is_skill_match(job_skill, resume_skill) for resume_skill in resume_skills_norm):
                missing.append(job_skill)
        
        return missing

import os
import re
from typing import List, Dict, Any
from datetime import datetime

def format_date(date_obj):
    """
    Format a datetime object as a string.
    
    Args:
        date_obj: The datetime object to format
        
    Returns:
        Formatted date string
    """
    if not date_obj:
        return ""
    
    return date_obj.strftime("%B %d, %Y")

def format_skills(skills_str):
    """
    Format a comma-separated skills string into a list.
    
    Args:
        skills_str: Comma-separated string of skills
        
    Returns:
        List of skills
    """
    if not skills_str:
        return []
    
    return [skill.strip() for skill in skills_str.split(',') if skill.strip()]

def extract_keywords(text):
    """
    Extract keywords from text by removing common words.
    
    Args:
        text: The text to extract keywords from
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Common words to exclude
    common_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
        'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'as', 'of',
        'that', 'this', 'these', 'those', 'it', 'they', 'them', 'their',
        'from', 'have', 'has', 'had', 'be', 'been', 'being', 'do', 'does',
        'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might'
    }
    
    # Split text into words, convert to lowercase, and remove punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out common words and short words
    keywords = [word for word in words if word not in common_words and len(word) > 2]
    
    return keywords

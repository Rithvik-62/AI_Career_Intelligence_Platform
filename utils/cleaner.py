"""
Module for text preprocessing and cleaning.
This module provides functions to clean and preprocess raw text data for NLP tasks.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List

# Ensure required NLTK resources are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
    
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4', quiet=True)


def clean_text(text: str) -> str:
    """
    Cleans raw text by applying a comprehensive NLP pipeline.
    
    The pipeline includes:
    1. Converting text to lowercase
    2. Removing URLs
    3. Removing email addresses
    4. Removing numbers
    5. Removing punctuation and special characters
    6. Removing extra spaces
    7. Removing stopwords
    8. Lemmatizing words
    
    Args:
        text (str): The raw input text.
        
    Returns:
        str: The cleaned, preprocessed text.
    """
    try:
        if not isinstance(text, str):
            return ""
            
        # 1. Convert text to lowercase
        text = text.lower()
        
        # 2. Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        # 3. Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # 4. Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Protect specific technical keywords with special characters
        replacements = {
            'c++': 'cplusplus',
            'c#': 'csharp',
            '.net': 'dotnet',
            'node.js': 'nodejs'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # 5. Remove punctuation and special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 6. Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 7. Remove stopwords & 8. Lemmatize words
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        words = text.split()
        
        # Filter stopwords and lemmatize
        cleaned_words = [
            lemmatizer.lemmatize(word) for word in words 
            if word not in stop_words
        ]
        
        # Return cleaned text as a single string
        return ' '.join(cleaned_words)
    except Exception as e:
        import sys
        sys.stderr.write(f"Error in clean_text: {str(e)}\n")
        return ""

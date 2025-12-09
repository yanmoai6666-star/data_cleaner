# Text Transformer
"""
Text transformation utilities.
"""

from typing import Any, List, Optional, Union
import re
import string
from collections import Counter

from .base_transformer import DataTransformer
from ..config import Config

class TextTransformer(DataTransformer):
    """
    Text transformation utility class.
    
    Attributes:
        lowercase (bool): Whether to convert text to lowercase.
        uppercase (bool): Whether to convert text to uppercase.
        capitalize (bool): Whether to capitalize the first letter.
        strip_punctuation (bool): Whether to remove punctuation.
        tokenize (bool): Whether to tokenize text into words.
        remove_stopwords (bool): Whether to remove stopwords.
        lemmatize (bool): Whether to lemmatize words.
        stem (bool): Whether to stem words.
        ngrams (Optional[int]): Size of n-grams to generate.
        stopwords (Set[str]): Set of stopwords to remove.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a TextTransformer instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.lowercase = self.config.get("text_transformer.lowercase", False)
        self.uppercase = self.config.get("text_transformer.uppercase", False)
        self.capitalize = self.config.get("text_transformer.capitalize", False)
        self.strip_punctuation = self.config.get("text_transformer.strip_punctuation", False)
        self.tokenize = self.config.get("text_transformer.tokenize", False)
        self.remove_stopwords = self.config.get("text_transformer.remove_stopwords", False)
        self.lemmatize = self.config.get("text_transformer.lemmatize", False)
        self.stem = self.config.get("text_transformer.stem", False)
        self.ngrams = self.config.get("text_transformer.ngrams", None)
        
        # Load stopwords
        self.stopwords = set(self.config.get("text_transformer.stopwords", [
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "with", "by", "of", "about", "as", "is", "was", "are", "were",
            "be", "been", "being", "have", "has", "had", "do", "does", "did"
        ]))
        
        # Initialize NLTK components if needed (lazy import to avoid dependency issues)
        self.nltk_initialized = False
        self.lemmatizer = None
        self.stemmer = None
    
    def _initialize_nltk(self):
        """
        Initialize NLTK components if needed.
        """
        if not self.nltk_initialized and (self.lemmatize or self.stem):
            try:
                import nltk
                nltk.download('wordnet', quiet=True)
                nltk.download('punkt', quiet=True)
                
                from nltk.stem import WordNetLemmatizer, PorterStemmer
                
                self.lemmatizer = WordNetLemmatizer()
                self.stemmer = PorterStemmer()
                self.nltk_initialized = True
            except ImportError:
                self.logger.warning("NLTK not installed. Lemmatization and stemming will be disabled.")
                self.lemmatize = False
                self.stem = False
            except Exception as e:
                self.logger.warning(f"Error initializing NLTK: {e}")
                self.lemmatize = False
                self.stem = False
    
    def transform(self, text: Any) -> Union[str, List[str], Optional[List[List[str]]]]:
        """
        Transform text data.
        
        Args:
            text (Any): Text to be transformed.
            
        Returns:
            Union[str, List[str], Optional[List[List[str]]]]: Transformed text, which could be a string, 
            a list of tokens, or a list of n-grams depending on configuration.
        """
        if text is None:
            return None
            
        # Convert to string
        try:
            transformed_text = str(text)
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
        
        # Apply text case transformations
        if self.lowercase:
            transformed_text = transformed_text.lower()
        elif self.uppercase:
            transformed_text = transformed_text.upper()
        elif self.capitalize:
            transformed_text = transformed_text.capitalize()
        
        # Remove punctuation
        if self.strip_punctuation:
            transformed_text = transformed_text.translate(str.maketrans("", "", string.punctuation))
        
        # Tokenize if configured
        if self.tokenize or self.remove_stopwords or self.lemmatize or self.stem or self.ngrams:
            # Split into tokens
            tokens = re.findall(r"\b\w+\b", transformed_text)
            
            # Remove stopwords
            if self.remove_stopwords:
                tokens = [token for token in tokens if token.lower() not in self.stopwords]
            
            # Initialize NLTK if needed
            self._initialize_nltk()
            
            # Lemmatize
            if self.lemmatize and self.lemmatizer:
                tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
            
            # Stem
            if self.stem and self.stemmer:
                tokens = [self.stemmer.stem(token) for token in tokens]
            
            # Generate n-grams
            if self.ngrams:
                if len(tokens) < self.ngrams:
                    return None
                ngrams = []
                for i in range(len(tokens) - self.ngrams + 1):
                    ngrams.append(tokens[i:i+self.ngrams])
                return ngrams
            
            # Return tokens if tokenize is enabled
            if self.tokenize:
                return tokens
            
            # Otherwise join back to string
            transformed_text = " ".join(tokens)
        
        return transformed_text
    
    def count_words(self, text: Any) -> Optional[Dict[str, int]]:
        """
        Count word frequencies in text.
        
        Args:
            text (Any): Text to count words in.
            
        Returns:
            Optional[Dict[str, int]]: Dictionary of word frequencies, or None if input is invalid.
        """
        transformed_text = self.transform(text)
        
        if isinstance(transformed_text, list):
            # If already tokenized
            tokens = transformed_text
        elif isinstance(transformed_text, str):
            # Tokenize the string
            tokens = re.findall(r"\b\w+\b", transformed_text.lower())
        else:
            return None
        
        return dict(Counter(tokens))
    
    def get_word_lengths(self, text: Any) -> Optional[List[int]]:
        """
        Get lengths of words in text.
        
        Args:
            text (Any): Text to analyze.
            
        Returns:
            Optional[List[int]]: List of word lengths, or None if input is invalid.
        """
        transformed_text = self.transform(text)
        
        if isinstance(transformed_text, list):
            # If already tokenized
            tokens = transformed_text
        elif isinstance(transformed_text, str):
            # Tokenize the string
            tokens = re.findall(r"\b\w+\b", transformed_text)
        else:
            return None
        
        return [len(token) for token in tokens]

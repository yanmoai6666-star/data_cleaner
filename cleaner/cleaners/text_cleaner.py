# Text Cleaner
"""
Text cleaning utilities.
"""

import re
from typing import Any, Optional

from .base_cleaner import DataCleaner
from ..config import Config

class TextCleaner(DataCleaner):
    """
    Text cleaning utility class.
    
    Attributes:
        lowercase (bool): Whether to convert text to lowercase.
        remove_special_chars (bool): Whether to remove special characters.
        remove_extra_spaces (bool): Whether to remove extra spaces.
        remove_newlines (bool): Whether to remove newlines.
        remove_digits (bool): Whether to remove digits.
        strip_whitespace (bool): Whether to strip whitespace from both ends.
        replace_patterns (dict): Dictionary of patterns to replace.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a TextCleaner instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.lowercase = self.config.get("text_cleaner.lowercase", True)
        self.remove_special_chars = self.config.get("text_cleaner.remove_special_chars", True)
        self.remove_extra_spaces = self.config.get("text_cleaner.remove_extra_spaces", True)
        self.remove_newlines = self.config.get("text_cleaner.remove_newlines", True)
        self.remove_digits = self.config.get("text_cleaner.remove_digits", False)
        self.strip_whitespace = self.config.get("text_cleaner.strip_whitespace", True)
        self.replace_patterns = self.config.get("text_cleaner.replace_patterns", {})
        
        # 编译正则表达式（新增表情符号和特殊符号匹配）
        self.special_chars_pattern = re.compile(
            r"[^a-zA-Z0-9\s]|[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF¤§]"
        )
        self.extra_spaces_pattern = re.compile(r"\s+")
        self.newlines_pattern = re.compile(r"[\r\n]+")
        self.digits_pattern = re.compile(r"\d+")
    
    def clean(self, text: Any) -> Optional[str]:
        """
        Clean text data.
        
        Args:
            text (Any): Text to be cleaned.
            
        Returns:
            Optional[str]: Cleaned text, or None if input is invalid.
        """
        if text is None:
            return None
            
        # Convert to string
        try:
            cleaned_text = str(text)
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
        
        # 新增特殊字符移除统计
        original_length = len(cleaned_text)
        
        # Apply cleaning operations based on configuration
        if self.lowercase:
            cleaned_text = cleaned_text.lower()
            
        if self.remove_special_chars:
            cleaned_text = self.special_chars_pattern.sub("", cleaned_text)
            
        if self.remove_extra_spaces:
            cleaned_text = self.extra_spaces_pattern.sub(" ", cleaned_text)
            
        if self.remove_newlines:
            cleaned_text = self.newlines_pattern.sub(" ", cleaned_text)
            
        if self.remove_digits:
            cleaned_text = self.digits_pattern.sub("", cleaned_text)
            
        if self.strip_whitespace:
            cleaned_text = cleaned_text.strip()
            
        # Apply custom replace patterns
        for pattern, replacement in self.replace_patterns.items():
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
        
        # 更新清洗统计（记录移除的特殊字符数量）
        removed_chars = original_length - len(cleaned_text)
        if hasattr(self, 'clean_stats'):
            self.clean_stats.setdefault("special_chars_removed", 0)
            self.clean_stats["special_chars_removed"] += removed_chars
        
        # Return None if text is empty after cleaning
        return cleaned_text if cleaned_text else None
    
    def clean_email(self, email: Any) -> Optional[str]:
        """
        Clean and validate email address.
        
        Args:
            email (Any): Email address to be cleaned.
            
        Returns:
            Optional[str]: Cleaned and validated email, or None if invalid.
        """
        cleaned_email = self.clean(email)
        if not cleaned_email:
            return None
            
        # Basic email validation
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if email_pattern.match(cleaned_email):
            return cleaned_email
        else:
            self.logger.warning(f"Invalid email format: {cleaned_email}")
            return None
    
    def clean_url(self, url: Any) -> Optional[str]:
        """
        Clean and validate URL.
        
        Args:
            url (Any): URL to be cleaned.
            
        Returns:
            Optional[str]: Cleaned and validated URL, or None if invalid.
        """
        cleaned_url = self.clean(url)
        if not cleaned_url:
            return None
            
        # Basic URL validation
        url_pattern = re.compile(r"^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$")
        if url_pattern.match(cleaned_url):
            # Add http:// if missing
            if not cleaned_url.startswith(("http://", "https://")):
                cleaned_url = f"http://{cleaned_url}"
            return cleaned_url
        else:
            self.logger.warning(f"Invalid URL format: {cleaned_url}")
            return None

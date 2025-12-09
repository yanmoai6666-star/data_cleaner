# Email Cleaner
"""
Email address cleaning utilities.
"""

import re
from typing import Any, Optional

from .base_cleaner import DataCleaner
from ..config import Config

class EmailCleaner(DataCleaner):
    """
    Email address cleaning utility class.
    
    Attributes:
        allow_subdomains (bool): Whether to allow subdomains.
        allow_special_chars (bool): Whether to allow special characters in local part.
        valid_domains (Optional[List[str]]): List of allowed domains, or None to allow all.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize an EmailCleaner instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.allow_subdomains = self.config.get("email_cleaner.allow_subdomains", True)
        self.allow_special_chars = self.config.get("email_cleaner.allow_special_chars", True)
        self.valid_domains = self.config.get("email_cleaner.valid_domains", None)
        
        # Compile regex patterns
        if self.allow_special_chars:
            # Allow common special characters in local part
            self.local_part_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+$")
        else:
            # Only allow alphanumeric and underscore
            self.local_part_pattern = re.compile(r"^[a-zA-Z0-9_]+$")
            
        if self.allow_subdomains:
            self.domain_pattern = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        else:
            self.domain_pattern = re.compile(r"^[a-zA-Z0-9]+\.[a-zA-Z]{2,}$")
        
        # Full email pattern
        self.email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    
    def clean(self, email: Any) -> Optional[str]:
        """
        Clean email address.
        
        Args:
            email (Any): Email address to be cleaned.
            
        Returns:
            Optional[str]: Cleaned email address, or None if input is invalid.
        """
        if email is None:
            return None
            
        # Convert to string and strip whitespace
        try:
            email_str = str(email).strip().lower()
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
        
        # Basic format validation
        if not self.email_pattern.match(email_str):
            self.logger.warning(f"Invalid email format: {email_str}")
            return None
        
        # Split into local part and domain
        local_part, domain = email_str.split("@", 1)
        
        # Validate local part
        if not self.local_part_pattern.match(local_part):
            self.logger.warning(f"Invalid local part in email: {local_part}")
            return None
        
        # Validate domain
        if not self.domain_pattern.match(domain):
            self.logger.warning(f"Invalid domain in email: {domain}")
            return None
        
        # Check if domain is in valid domains list
        if self.valid_domains and domain not in self.valid_domains:
            self.logger.warning(f"Domain not allowed: {domain}")
            return None
        
        # Check for common disposable email domains
        disposable_domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
            "protonmail.com", "aol.com", "mail.com", "yandex.com", "zoho.com"
        ]
        
        if domain in disposable_domains:
            self.logger.info(f"Disposable email domain detected: {domain}")
            # We still return it, just log the information
        
        return email_str
    
    def extract_domain(self, email: Any) -> Optional[str]:
        """
        Extract domain from email address.
        
        Args:
            email (Any): Email address.
            
        Returns:
            Optional[str]: Extracted domain, or None if email is invalid.
        """
        cleaned_email = self.clean(email)
        if cleaned_email:
            return cleaned_email.split("@", 1)[1]
        return None
    
    def extract_local_part(self, email: Any) -> Optional[str]:
        """
        Extract local part from email address.
        
        Args:
            email (Any): Email address.
            
        Returns:
            Optional[str]: Extracted local part, or None if email is invalid.
        """
        cleaned_email = self.clean(email)
        if cleaned_email:
            return cleaned_email.split("@", 1)[0]
        return None

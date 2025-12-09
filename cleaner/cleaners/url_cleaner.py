# URL Cleaner
"""
URL cleaning utilities.
"""

import re
from typing import Any, Optional
from urllib.parse import urlparse, urlunparse

from .base_cleaner import DataCleaner
from ..config import Config

class URLCleaner(DataCleaner):
    """
    URL cleaning utility class.
    
    Attributes:
        add_scheme (bool): Whether to add http:// if no scheme is present.
        allowed_schemes (List[str]): List of allowed schemes.
        remove_www (bool): Whether to remove www prefix.
        remove_query_params (bool): Whether to remove query parameters.
        remove_fragments (bool): Whether to remove fragments.
        valid_domains (Optional[List[str]]): List of allowed domains, or None to allow all.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a URLCleaner instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.add_scheme = self.config.get("url_cleaner.add_scheme", True)
        self.allowed_schemes = self.config.get("url_cleaner.allowed_schemes", ["http", "https"])
        self.remove_www = self.config.get("url_cleaner.remove_www", False)
        self.remove_query_params = self.config.get("url_cleaner.remove_query_params", False)
        self.remove_fragments = self.config.get("url_cleaner.remove_fragments", True)
        self.valid_domains = self.config.get("url_cleaner.valid_domains", None)
        
        # Compile regex patterns
        self.url_pattern = re.compile(r"^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$")
        self.www_pattern = re.compile(r"^www\.")
    
    def clean(self, url: Any) -> Optional[str]:
        """
        Clean URL address.
        
        Args:
            url (Any): URL to be cleaned.
            
        Returns:
            Optional[str]: Cleaned URL, or None if input is invalid.
        """
        if url is None:
            return None
            
        # Convert to string and strip whitespace
        try:
            url_str = str(url).strip()
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
        
        # Basic format validation
        if not self.url_pattern.match(url_str):
            self.logger.warning(f"Invalid URL format: {url_str}")
            return None
        
        # Add scheme if not present
        if self.add_scheme and not url_str.startswith(("http://", "https://")):
            url_str = f"http://{url_str}"
        
        # Parse URL components
        parsed = urlparse(url_str)
        
        # Validate scheme
        if parsed.scheme not in self.allowed_schemes:
            self.logger.warning(f"Scheme not allowed: {parsed.scheme}")
            return None
        
        # Remove www prefix if configured
        if self.remove_www:
            netloc = self.www_pattern.sub("", parsed.netloc)
        else:
            netloc = parsed.netloc
        
        # Validate domain if valid_domains is configured
        if self.valid_domains:
            # Extract domain name without subdomains
            domain_parts = netloc.split(".")
            if len(domain_parts) >= 2:
                domain = ".".join(domain_parts[-2:])
                if domain not in self.valid_domains:
                    self.logger.warning(f"Domain not allowed: {domain}")
                    return None
        
        # Remove query params if configured
        query = "" if self.remove_query_params else parsed.query
        
        # Remove fragments if configured
        fragment = "" if self.remove_fragments else parsed.fragment
        
        # Reconstruct URL
        cleaned_url = urlunparse((
            parsed.scheme,
            netloc,
            parsed.path,
            parsed.params,
            query,
            fragment
        ))
        
        return cleaned_url
    
    def extract_domain(self, url: Any) -> Optional[str]:
        """
        Extract domain from URL.
        
        Args:
            url (Any): URL to extract domain from.
            
        Returns:
            Optional[str]: Extracted domain, or None if URL is invalid.
        """
        cleaned_url = self.clean(url)
        if cleaned_url:
            parsed = urlparse(cleaned_url)
            return parsed.netloc
        return None
    
    def extract_path(self, url: Any) -> Optional[str]:
        """
        Extract path from URL.
        
        Args:
            url (Any): URL to extract path from.
            
        Returns:
            Optional[str]: Extracted path, or None if URL is invalid.
        """
        cleaned_url = self.clean(url)
        if cleaned_url:
            parsed = urlparse(cleaned_url)
            return parsed.path
        return None

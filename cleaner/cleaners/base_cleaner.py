# Base Cleaner Class
"""
Base class for all data cleaners.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..config import Config
from ..utils.logging_config import setup_logging

class DataCleaner(ABC):
    """
    Base class for data cleaning operations.
    
    Attributes:
        config (Config): Configuration object.
        logger (logging.Logger): Logger instance.
        clean_stats (Dict): Statistics about cleaning operations.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a DataCleaner instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        from ..config import get_default_config
        self.config = config or get_default_config()
        self.logger = setup_logging(self.__class__.__name__)
        self.clean_stats = {
            "total_records": 0,
            "cleaned_records": 0,
            "removed_records": 0,
            "errors": 0
        }
    
    @abstractmethod
    def clean(self, data: Any) -> Any:
        """
        Abstract method to clean data.
        
        Args:
            data (Any): Data to be cleaned.
            
        Returns:
            Any: Cleaned data.
        """
        pass
    
    def validate(self, data: Any) -> bool:
        """
        Validate if data is clean.
        
        Args:
            data (Any): Data to validate.
            
        Returns:
            bool: True if data is clean, False otherwise.
        """
        try:
            cleaned_data = self.clean(data)
            return cleaned_data is not None
        except Exception:
            return False
    
    def clean_batch(self, data_list: List[Any]) -> List[Any]:
        """
        Clean a batch of data.
        
        Args:
            data_list (List[Any]): List of data to be cleaned.
            
        Returns:
            List[Any]: List of cleaned data.
        """
        self.clean_stats["total_records"] = len(data_list)
        cleaned_list = []
        
        for data in data_list:
            try:
                cleaned_data = self.clean(data)
                if cleaned_data is not None:
                    cleaned_list.append(cleaned_data)
                    self.clean_stats["cleaned_records"] += 1
                else:
                    self.clean_stats["removed_records"] += 1
            except Exception as e:
                self.logger.error(f"Error cleaning data: {e}")
                self.clean_stats["errors"] += 1
                self.clean_stats["removed_records"] += 1
        
        self.logger.info(f"Batch cleaning completed. Stats: {self.clean_stats}")
        return cleaned_list
    
    def get_stats(self) -> Dict:
        """
        Get cleaning statistics.
        
        Returns:
            Dict: Cleaning statistics.
        """
        return self.clean_stats
    
    def reset_stats(self) -> None:
        """
        Reset cleaning statistics.
        """
        self.clean_stats = {
            "total_records": 0,
            "cleaned_records": 0,
            "removed_records": 0,
            "errors": 0
        }

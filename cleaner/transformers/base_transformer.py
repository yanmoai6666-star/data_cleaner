# Base Transformer Class
"""
Base class for all data transformers.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..config import Config
from ..utils.logging_config import setup_logging

class DataTransformer(ABC):
    """
    Base class for data transformation operations.
    
    Attributes:
        config (Config): Configuration object.
        logger (logging.Logger): Logger instance.
        transform_stats (Dict): Statistics about transformation operations.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a DataTransformer instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        from ..config import get_default_config
        self.config = config or get_default_config()
        self.logger = setup_logging(self.__class__.__name__)
        self.transform_stats = {
            "total_records": 0,
            "transformed_records": 0,
            "errors": 0
        }
    
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        Abstract method to transform data.
        
        Args:
            data (Any): Data to be transformed.
            
        Returns:
            Any: Transformed data.
        """
        pass
    
    def transform_batch(self, data_list: List[Any]) -> List[Any]:
        """
        Transform a batch of data.
        
        Args:
            data_list (List[Any]): List of data to be transformed.
            
        Returns:
            List[Any]: List of transformed data.
        """
        self.transform_stats["total_records"] = len(data_list)
        transformed_list = []
        
        for data in data_list:
            try:
                transformed_data = self.transform(data)
                transformed_list.append(transformed_data)
                self.transform_stats["transformed_records"] += 1
            except Exception as e:
                self.logger.error(f"Error transforming data: {e}")
                transformed_list.append(None)
                self.transform_stats["errors"] += 1
        
        self.logger.info(f"Batch transformation completed. Stats: {self.transform_stats}")
        return transformed_list
    
    def get_stats(self) -> Dict:
        """
        Get transformation statistics.
        
        Returns:
            Dict: Transformation statistics.
        """
        return self.transform_stats
    
    def reset_stats(self) -> None:
        """
        Reset transformation statistics.
        """
        self.transform_stats = {
            "total_records": 0,
            "transformed_records": 0,
            "errors": 0
        }
    
    def fit(self, data_list: List[Any]) -> "DataTransformer":
        """
        Fit the transformer to the data (for transformers that need to learn from data).
        
        Args:
            data_list (List[Any]): List of data to fit to.
            
        Returns:
            DataTransformer: Self for method chaining.
        """
        # Default implementation does nothing
        return self
    
    def fit_transform(self, data_list: List[Any]) -> List[Any]:
        """
        Fit the transformer to the data and then transform it.
        
        Args:
            data_list (List[Any]): List of data to fit to and transform.
            
        Returns:
            List[Any]: List of transformed data.
        """
        return self.fit(data_list).transform_batch(data_list)

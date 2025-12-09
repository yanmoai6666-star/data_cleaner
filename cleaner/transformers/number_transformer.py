# Number Transformer
"""
Number transformation utilities.
"""

from typing import Any, Dict, List, Optional, Union
import math

from .base_transformer import DataTransformer
from ..config import Config
from ..cleaners.number_cleaner import NumberCleaner

class NumberTransformer(DataTransformer):
    """
    Number transformation utility class.
    
    Attributes:
        normalize (bool): Whether to normalize numbers to [0, 1] range.
        standardize (bool): Whether to standardize numbers (z-score).
        discretize (bool): Whether to discretize numbers into bins.
        log_transform (bool): Whether to apply log transformation.
        bin_count (int): Number of bins for discretization.
        min_value (Optional[float]): Minimum value for normalization.
        max_value (Optional[float]): Maximum value for normalization.
        mean (Optional[float]): Mean value for standardization.
        std (Optional[float]): Standard deviation for standardization.
        bins (Optional[List[float]]): Bin boundaries for discretization.
        number_cleaner (NumberCleaner): Instance of NumberCleaner for preprocessing.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a NumberTransformer instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.normalize = self.config.get("number_transformer.normalize", False)
        self.standardize = self.config.get("number_transformer.standardize", False)
        self.discretize = self.config.get("number_transformer.discretize", False)
        self.log_transform = self.config.get("number_transformer.log_transform", False)
        self.bin_count = self.config.get("number_transformer.bin_count", 5)
        
        # Statistical parameters (will be set during fit)
        self.min_value = self.config.get("number_transformer.min_value", None)
        self.max_value = self.config.get("number_transformer.max_value", None)
        self.mean = self.config.get("number_transformer.mean", None)
        self.std = self.config.get("number_transformer.std", None)
        self.bins = self.config.get("number_transformer.bins", None)
        
        # Create a NumberCleaner instance for preprocessing
        self.number_cleaner = NumberCleaner(config)
        
        # Data storage for fit method
        self.data = []
    
    def fit(self, data_list: List[Any]) -> "NumberTransformer":
        """
        Fit the transformer to the data.
        
        Args:
            data_list (List[Any]): List of data to fit to.
            
        Returns:
            NumberTransformer: Self for method chaining.
        """
        # Clean and filter the data
        cleaned_data = []
        for data in data_list:
            cleaned = self.number_cleaner.clean(data)
            if cleaned is not None:
                cleaned_data.append(cleaned)
        
        self.data = cleaned_data
        
        # Calculate min and max for normalization
        if self.normalize and self.min_value is None and self.max_value is None:
            if cleaned_data:
                self.min_value = min(cleaned_data)
                self.max_value = max(cleaned_data)
        
        # Calculate mean and std for standardization
        if self.standardize and self.mean is None and self.std is None:
            if cleaned_data:
                self.mean = sum(cleaned_data) / len(cleaned_data)
                variance = sum((x - self.mean) ** 2 for x in cleaned_data) / len(cleaned_data)
                self.std = math.sqrt(variance)
        
        # Create bins for discretization
        if self.discretize and self.bins is None:
            if cleaned_data:
                self.min_value = min(cleaned_data) if self.min_value is None else self.min_value
                self.max_value = max(cleaned_data) if self.max_value is None else self.max_value
                bin_width = (self.max_value - self.min_value) / self.bin_count
                self.bins = [self.min_value + i * bin_width for i in range(self.bin_count + 1)]
        
        return self
    
    def transform(self, data: Any) -> Optional[Union[float, int, str]]:
        """
        Transform number data.
        
        Args:
            data (Any): Number to be transformed.
            
        Returns:
            Optional[Union[float, int, str]]: Transformed number, or None if input is invalid.
        """
        # Clean the number first
        cleaned_num = self.number_cleaner.clean(data)
        if cleaned_num is None:
            return None
        
        transformed_num = cleaned_num
        
        # Apply log transformation
        if self.log_transform:
            if transformed_num <= 0:
                self.logger.warning(f"Log transformation requires positive numbers, got {transformed_num}")
            else:
                transformed_num = math.log(transformed_num)
        
        # Apply normalization
        if self.normalize:
            if self.min_value is None or self.max_value is None:
                self.logger.warning("Normalization requires min and max values. Call fit() first.")
            elif self.max_value == self.min_value:
                transformed_num = 0.0
            else:
                transformed_num = (transformed_num - self.min_value) / (self.max_value - self.min_value)
        
        # Apply standardization
        if self.standardize:
            if self.mean is None or self.std is None:
                self.logger.warning("Standardization requires mean and std values. Call fit() first.")
            elif self.std == 0:
                transformed_num = 0.0
            else:
                transformed_num = (transformed_num - self.mean) / self.std
        
        # Apply discretization
        if self.discretize:
            if self.bins is None:
                self.logger.warning("Discretization requires bins. Call fit() first.")
            else:
                for i in range(len(self.bins) - 1):
                    if self.bins[i] <= transformed_num <= self.bins[i+1]:
                        transformed_num = f"Bin {i+1}"
                        break
                # Handle values outside bins
                if isinstance(transformed_num, (int, float)):
                    if transformed_num < self.bins[0]:
                        transformed_num = f"Bin 0"
                    else:
                        transformed_num = f"Bin {len(self.bins)}"
        
        return transformed_num
    
    def get_statistics(self) -> Dict:
        """
        Get statistics of the fitted data.
        
        Returns:
            Dict: Statistics dictionary.
        """
        stats = {
            "count": len(self.data),
            "min": self.min_value,
            "max": self.max_value,
            "mean": self.mean,
            "std": self.std
        }
        
        if self.data:
            # Calculate median
            sorted_data = sorted(self.data)
            n = len(sorted_data)
            if n % 2 == 0:
                median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            else:
                median = sorted_data[n//2]
            stats["median"] = median
            
            # Calculate quartiles
            q1 = sorted_data[n//4]
            q3 = sorted_data[3*n//4]
            stats["q1"] = q1
            stats["q3"] = q3
        
        return stats

# Categorical Transformer
"""
Categorical data transformation utilities.
"""

from typing import Any, Dict, List, Optional, Union
from collections import Counter

from .base_transformer import DataTransformer
from ..config import Config

class CategoricalTransformer(DataTransformer):
    """
    Categorical data transformation utility class.
    
    Attributes:
        encoding_type (str): Type of encoding to use ('one-hot', 'label', 'frequency').
        categories (Optional[List[str]]): List of allowed categories.
        max_categories (Optional[int]): Maximum number of categories to keep.
        unknown_category (Optional[str]): Category to use for unknown values.
        category_map (Dict[str, Any]): Mapping of categories to encoded values.
        most_common (List[str]): List of most common categories.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a CategoricalTransformer instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.encoding_type = self.config.get("categorical_transformer.encoding_type", "label")
        self.categories = self.config.get("categorical_transformer.categories", None)
        self.max_categories = self.config.get("categorical_transformer.max_categories", None)
        self.unknown_category = self.config.get("categorical_transformer.unknown_category", "Unknown")
        
        # Initialize category mapping
        self.category_map = {}
        self.most_common = []
    
    def fit(self, data_list: List[Any]) -> "CategoricalTransformer":
        """
        Fit the transformer to the data.
        
        Args:
            data_list (List[Any]): List of data to fit to.
            
        Returns:
            CategoricalTransformer: Self for method chaining.
        """
        # Convert to string and filter None values
        str_data = [str(data) for data in data_list if data is not None]
        
        # Count category frequencies
        category_counts = Counter(str_data)
        
        # Determine categories to use
        if self.categories is None:
            if self.max_categories:
                # Keep only the most common categories
                self.most_common = [cat for cat, count in category_counts.most_common(self.max_categories)]
                self.categories = self.most_common
                if len(category_counts) > self.max_categories:
                    self.logger.info(f"Keeping only top {self.max_categories} categories out of {len(category_counts)}")
            else:
                # Use all categories
                self.categories = list(category_counts.keys())
        
        # Create encoding mapping based on encoding type
        if self.encoding_type == "label":
            # Label encoding: map each category to an integer
            for i, category in enumerate(self.categories):
                self.category_map[category] = i
            # Add unknown category mapping
            if self.unknown_category and self.unknown_category not in self.category_map:
                self.category_map[self.unknown_category] = len(self.categories)
                
        elif self.encoding_type == "frequency":
            # Frequency encoding: map each category to its frequency
            total = sum(category_counts.values())
            for category in self.categories:
                self.category_map[category] = category_counts[category] / total
            # Add unknown category mapping
            if self.unknown_category and self.unknown_category not in self.category_map:
                self.category_map[self.unknown_category] = 0.0
                
        elif self.encoding_type == "one-hot":
            # One-hot encoding: map each category to a binary vector
            # This will be handled during transformation, not during fitting
            pass
        
        return self
    
    def transform(self, data: Any) -> Optional[Union[int, float, Dict[str, int]]]:
        """
        Transform categorical data.
        
        Args:
            data (Any): Categorical data to be transformed.
            
        Returns:
            Optional[Union[int, float, Dict[str, int]]]: Transformed data, which could be an integer (label encoding),
            a float (frequency encoding), or a dictionary (one-hot encoding), or None if input is invalid.
        """
        if data is None:
            return None
            
        # Convert to string
        try:
            category = str(data)
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
        
        # Handle unknown categories
        if category not in self.categories:
            if self.unknown_category:
                category = self.unknown_category
            else:
                self.logger.warning(f"Unknown category: {category}")
                return None
        
        # Apply encoding
        if self.encoding_type == "one-hot":
            # One-hot encoding
            one_hot = {}
            for cat in self.categories:
                one_hot[cat] = 1 if cat == category else 0
            # Add unknown category indicator if applicable
            if self.unknown_category:
                one_hot[self.unknown_category] = 1 if category == self.unknown_category else 0
            return one_hot
            
        elif category in self.category_map:
            # Label or frequency encoding
            return self.category_map[category]
        
        return None
    
    def get_category_counts(self) -> Dict[str, int]:
        """
        Get category counts from the fitted data.
        
        Returns:
            Dict[str, int]: Dictionary of category counts.
        """
        # This would be more accurate if we stored the counts during fit
        # For now, we'll return a dummy dictionary based on categories
        return {cat: 0 for cat in self.categories}
    
    def get_unknown_percentage(self, data_list: List[Any]) -> float:
        """
        Calculate the percentage of unknown categories in a dataset.
        
        Args:
            data_list (List[Any]): List of data to analyze.
            
        Returns:
            float: Percentage of unknown categories.
        """
        if not data_list:
            return 0.0
            
        unknown_count = 0
        for data in data_list:
            if data is None:
                continue
            try:
                category = str(data)
                if category not in self.categories:
                    unknown_count += 1
            except:
                unknown_count += 1
        
        return (unknown_count / len(data_list)) * 100

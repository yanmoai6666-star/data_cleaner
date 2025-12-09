# Number Cleaner
"""
Number cleaning utilities.
"""

import re
from typing import Any, Optional, Union

from .base_cleaner import DataCleaner
from ..config import Config

class NumberCleaner(DataCleaner):
    """
    Number cleaning utility class.
    
    Attributes:
        remove_formatting (bool): Whether to remove formatting characters like commas.
        default_type (type): Default type to convert numbers to (int or float).
        min_value (Optional[float]): Minimum allowed value.
        max_value (Optional[float]): Maximum allowed value.
        allow_negative (bool): Whether to allow negative numbers.
        allow_decimal (bool): Whether to allow decimal numbers.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a NumberCleaner instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.remove_formatting = self.config.get("number_cleaner.remove_formatting", True)
        self.default_type = int if self.config.get("number_cleaner.default_type", "int") == "int" else float
        self.min_value = self.config.get("number_cleaner.min_value", None)
        self.max_value = self.config.get("number_cleaner.max_value", None)
        self.allow_negative = self.config.get("number_cleaner.allow_negative", True)
        self.allow_decimal = self.config.get("number_cleaner.allow_decimal", True)
        
        # Compile regex pattern for formatting removal
        self.formatting_pattern = re.compile(r"[^\d.-]")
    
    def clean(self, number: Any) -> Optional[Union[int, float]]:
        """
        Clean number data.
        
        Args:
            number (Any): Number to be cleaned.
            
        Returns:
            Optional[Union[int, float]]: Cleaned number, or None if input is invalid.
        """
        if number is None:
            return None
            
        # Convert to string first for cleaning
        try:
            number_str = str(number)
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
        
        # Remove formatting characters
        if self.remove_formatting:
            number_str = self.formatting_pattern.sub("", number_str)
        
        # Validate and convert to number
        try:
            # Check if it's a valid number format
            if not re.match(r"^-?\d+(\.\d+)?$", number_str):
                self.logger.warning(f"Invalid number format: {number_str}")
                return None
            
            # Convert to float first for validation
            float_num = float(number_str)
            
            # Check negative numbers
            if not self.allow_negative and float_num < 0:
                self.logger.warning(f"Negative numbers not allowed: {float_num}")
                return None
            
            # Check decimal numbers
            if not self.allow_decimal and float_num % 1 != 0:
                self.logger.warning(f"Decimal numbers not allowed: {float_num}")
                return None
            
            # Check range constraints
            if self.min_value is not None and float_num < self.min_value:
                self.logger.warning(f"Number below minimum value {self.min_value}: {float_num}")
                return None
            
            if self.max_value is not None and float_num > self.max_value:
                self.logger.warning(f"Number above maximum value {self.max_value}: {float_num}")
                return None
            
            # Convert to the default type
            if self.default_type == int:
                return int(float_num)
            else:
                return float_num
                
        except Exception as e:
            self.logger.error(f"Error processing number {number_str}: {e}")
            return None
    
    def clean_currency(self, currency: Any, currency_symbol: str = "$") -> Optional[Union[int, float]]:
        """
        Clean currency values.
        
        Args:
            currency (Any): Currency value to be cleaned.
            currency_symbol (str): Currency symbol to remove.
            
        Returns:
            Optional[Union[int, float]]: Cleaned currency value, or None if invalid.
        """
        if currency is None:
            return None
            
        # Remove currency symbol
        try:
            currency_str = str(currency).replace(currency_symbol, "")
        except Exception as e:
            self.logger.error(f"Error processing currency: {e}")
            return None
            
        # Use regular clean method for the rest
        return self.clean(currency_str)
    
    def clean_percentage(self, percentage: Any) -> Optional[Union[int, float]]:
        """
        Clean percentage values.
        
        Args:
            percentage (Any): Percentage value to be cleaned.
            
        Returns:
            Optional[Union[int, float]]: Cleaned percentage value (as decimal), or None if invalid.
        """
        if percentage is None:
            return None
            
        # Remove percentage symbol
        try:
            percentage_str = str(percentage).replace("%", "")
        except Exception as e:
            self.logger.error(f"Error processing percentage: {e}")
            return None
            
        # Clean as regular number
        cleaned_num = self.clean(percentage_str)
        
        # Convert to decimal if valid
        if cleaned_num is not None:
            return cleaned_num / 100
        else:
            return None

# DateTime Transformer
"""
Date and time transformation utilities.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import dateutil.parser as parser

from .base_transformer import DataTransformer
from ..config import Config
from ..cleaners.datetime_cleaner import DateTimeCleaner

class DateTimeTransformer(DataTransformer):
    """
    Date and time transformation utility class.
    
    Attributes:
        output_format (str): Desired output format.
        extract_components (bool): Whether to extract individual date/time components.
        components_to_extract (List[str]): List of components to extract.
        calculate_durations (bool): Whether to calculate durations from a reference date.
        reference_date (Optional[datetime]): Reference date for duration calculations.
        datetime_cleaner (DateTimeCleaner): Instance of DateTimeCleaner for preprocessing.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a DateTimeTransformer instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.output_format = self.config.get("datetime_transformer.output_format", "%Y-%m-%d %H:%M:%S")
        self.extract_components = self.config.get("datetime_transformer.extract_components", False)
        self.components_to_extract = self.config.get("datetime_transformer.components_to_extract", [
            "year", "month", "day", "hour", "minute", "second", "weekday"
        ])
        self.calculate_durations = self.config.get("datetime_transformer.calculate_durations", False)
        
        # Parse reference date if provided
        self.reference_date = None
        if self.config.get("datetime_transformer.reference_date"):
            try:
                self.reference_date = parser.parse(self.config["datetime_transformer.reference_date"])
            except Exception as e:
                self.logger.warning(f"Invalid reference_date format: {e}")
        
        # Create a DateTimeCleaner instance for preprocessing
        self.datetime_cleaner = DateTimeCleaner(config)
    
    def transform(self, data: Any) -> Optional[Union[str, Dict[str, Any]]]:
        """
        Transform date/time data.
        
        Args:
            data (Any): Date/time to be transformed.
            
        Returns:
            Optional[Union[str, Dict[str, Any]]]: Transformed date/time, which could be a formatted string
            or a dictionary of extracted components, or None if input is invalid.
        """
        # Clean the date/time first
        cleaned_datetime_str = self.datetime_cleaner.clean(data)
        if cleaned_datetime_str is None:
            return None
        
        # Parse to datetime object for further processing
        try:
            dt_obj = parser.parse(cleaned_datetime_str)
        except Exception as e:
            self.logger.error(f"Error parsing datetime: {e}")
            return None
        
        # Extract components if configured
        if self.extract_components:
            components = {}
            
            if "year" in self.components_to_extract:
                components["year"] = dt_obj.year
                
            if "month" in self.components_to_extract:
                components["month"] = dt_obj.month
                
            if "day" in self.components_to_extract:
                components["day"] = dt_obj.day
                
            if "hour" in self.components_to_extract:
                components["hour"] = dt_obj.hour
                
            if "minute" in self.components_to_extract:
                components["minute"] = dt_obj.minute
                
            if "second" in self.components_to_extract:
                components["second"] = dt_obj.second
                
            if "weekday" in self.components_to_extract:
                components["weekday"] = dt_obj.weekday()  # Monday=0, Sunday=6
                
            if "is_weekend" in self.components_to_extract:
                components["is_weekend"] = dt_obj.weekday() >= 5  # Saturday=5, Sunday=6
                
            if "quarter" in self.components_to_extract:
                components["quarter"] = (dt_obj.month - 1) // 3 + 1
                
            # Calculate durations if configured
            if self.calculate_durations and self.reference_date:
                duration = dt_obj - self.reference_date
                components["duration_days"] = duration.days
                components["duration_seconds"] = duration.total_seconds()
            
            return components
        
        # Otherwise, return formatted string
        return dt_obj.strftime(self.output_format)
    
    def get_age(self, birth_date: Any, reference_date: Any = None) -> Optional[int]:
        """
        Calculate age from birth date.
        
        Args:
            birth_date (Any): Birth date to calculate age from.
            reference_date (Any, optional): Reference date to calculate age against. If None, current date is used.
            
        Returns:
            Optional[int]: Calculated age, or None if input is invalid.
        """
        # Clean birth date
        birth_date_str = self.datetime_cleaner.clean(birth_date)
        if birth_date_str is None:
            return None
        
        try:
            birth_dt = parser.parse(birth_date_str)
        except Exception as e:
            self.logger.error(f"Error parsing birth date: {e}")
            return None
        
        # Get reference date
        if reference_date:
            ref_date_str = self.datetime_cleaner.clean(reference_date)
            if ref_date_str is None:
                return None
            try:
                ref_dt = parser.parse(ref_date_str)
            except Exception as e:
                self.logger.error(f"Error parsing reference date: {e}")
                return None
        else:
            ref_dt = datetime.now()
        
        # Calculate age
        age = ref_dt.year - birth_dt.year
        
        # Adjust if birthday hasn't occurred yet this year
        if (ref_dt.month, ref_dt.day) < (birth_dt.month, birth_dt.day):
            age -= 1
            
        return age

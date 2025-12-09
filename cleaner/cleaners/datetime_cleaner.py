# DateTime Cleaner
"""
Date and time cleaning utilities.
"""

from datetime import datetime
from typing import Any, Optional, Union
import dateutil.parser as parser

from .base_cleaner import DataCleaner
from ..config import Config

class DateTimeCleaner(DataCleaner):
    """
    Date and time cleaning utility class.
    
    Attributes:
        input_formats (List[str]): List of expected input formats.
        output_format (str): Desired output format.
        min_datetime (Optional[datetime]): Minimum allowed datetime.
        max_datetime (Optional[datetime]): Maximum allowed datetime.
        allow_future (bool): Whether to allow future dates.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize a DateTimeCleaner instance.
        
        Args:
            config (Config, optional): Configuration object. If None, default config is used.
        """
        super().__init__(config)
        
        # Get configuration from config object
        self.input_formats = self.config.get("datetime_cleaner.input_formats", [
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y",
            "%d/%m/%Y %H:%M:%S"
        ])
        self.output_format = self.config.get("datetime_cleaner.output_format", "%Y-%m-%d %H:%M:%S")
        
        # Parse min and max datetime if provided
        self.min_datetime = None
        if self.config.get("datetime_cleaner.min_datetime"):
            try:
                self.min_datetime = parser.parse(self.config["datetime_cleaner.min_datetime"])
            except Exception as e:
                self.logger.warning(f"Invalid min_datetime format: {e}")
                
        self.max_datetime = None
        if self.config.get("datetime_cleaner.max_datetime"):
            try:
                self.max_datetime = parser.parse(self.config["datetime_cleaner.max_datetime"])
            except Exception as e:
                self.logger.warning(f"Invalid max_datetime format: {e}")
                
        self.allow_future = self.config.get("datetime_cleaner.allow_future", True)
    
    def clean(self, datetime_str: Any) -> Optional[str]:
        """
        Clean date and time data.
        
        Args:
            datetime_str (Any): Date/time string to be cleaned.
            
        Returns:
            Optional[str]: Cleaned and formatted date/time string, or None if input is invalid.
        """
        if datetime_str is None:
            return None
            
        # Convert to string first
        try:
            dt_str = str(datetime_str)
        except Exception as e:
            self.logger.error(f"Error converting to string: {e}")
            return None
            
        # Try to parse with known formats first
        parsed_dt = None
        
        # Try each input format
        for fmt in self.input_formats:
            try:
                parsed_dt = datetime.strptime(dt_str, fmt)
                break
            except ValueError:
                continue
        
        # If no format matched, try dateutil parser
        if parsed_dt is None:
            try:
                parsed_dt = parser.parse(dt_str)
            except Exception as e:
                self.logger.warning(f"Could not parse datetime: {dt_str}. Error: {e}")
                return None
        
        # Validate datetime
        if not self.allow_future and parsed_dt > datetime.now():
            self.logger.warning(f"Future dates not allowed: {parsed_dt}")
            return None
            
        if self.min_datetime and parsed_dt < self.min_datetime:
            self.logger.warning(f"Datetime below minimum: {parsed_dt} < {self.min_datetime}")
            return None
            
        if self.max_datetime and parsed_dt > self.max_datetime:
            self.logger.warning(f"Datetime above maximum: {parsed_dt} > {self.max_datetime}")
            return None
        
        # Format to output format
        return parsed_dt.strftime(self.output_format)
    
    def clean_date(self, date_str: Any) -> Optional[str]:
        """
        Clean date data (without time).
        
        Args:
            date_str (Any): Date string to be cleaned.
            
        Returns:
            Optional[str]: Cleaned and formatted date string, or None if input is invalid.
        """
        # Save current output format
        original_output_format = self.output_format
        
        # Set output format to date only
        self.output_format = "%Y-%m-%d"
        
        # Clean using the main method
        cleaned_date = self.clean(date_str)
        
        # Restore original output format
        self.output_format = original_output_format
        
        return cleaned_date
    
    def clean_time(self, time_str: Any) -> Optional[str]:
        """
        Clean time data (without date).
        
        Args:
            time_str (Any): Time string to be cleaned.
            
        Returns:
            Optional[str]: Cleaned and formatted time string, or None if input is invalid.
        """
        if time_str is None:
            return None
            
        try:
            # Add a dummy date to use the main clean method
            dt_str = f"2000-01-01 {time_str}"
            
            # Save current output format
            original_output_format = self.output_format
            
            # Set output format to time only
            self.output_format = "%H:%M:%S"
            
            # Clean using the main method
            cleaned_time = self.clean(dt_str)
            
            # Restore original output format
            self.output_format = original_output_format
            
            return cleaned_time
            
        except Exception as e:
            self.logger.error(f"Error cleaning time: {e}")
            return None

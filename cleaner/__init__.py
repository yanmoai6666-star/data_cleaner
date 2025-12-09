# Data Cleaner Package
"""
A comprehensive data cleaning library for Python with various cleaning and transformation utilities.
"""

__version__ = "1.0.0"
__author__ = "Data Cleaning Team"
__email__ = "contact@datacleaner.com"

# Import main components from submodules
from .cleaners import (
    DataCleaner,
    TextCleaner,
    NumberCleaner,
    DateTimeCleaner,
    EmailCleaner,
    URLCleaner
)

from .transformers import (
    DataTransformer,
    TextTransformer,
    NumberTransformer,
    DateTimeTransformer,
    CategoricalTransformer
)

from .utils import (
    load_data,
    save_data,
    validate_data,
    generate_report,
    logging_config
)

from .config import (
    Config,
    get_default_config,
    load_config
)

# Package-level constants
DEFAULT_ENCODING = "utf-8"
DEFAULT_SEPARATOR = ","
DEFAULT_DATE_FORMAT = "%Y-%m-%d"

# Main entry point function
def create_cleaner(config=None):
    """
    Create a DataCleaner instance with the given configuration.
    
    Args:
        config (Config, optional): Configuration object. If None, default config is used.
    
    Returns:
        DataCleaner: Configured DataCleaner instance.
    """
    if config is None:
        config = get_default_config()
    return DataCleaner(config)

def create_transformer(config=None):
    """
    Create a DataTransformer instance with the given configuration.
    
    Args:
        config (Config, optional): Configuration object. If None, default config is used.
    
    Returns:
        DataTransformer: Configured DataTransformer instance.
    """
    if config is None:
        config = get_default_config()
    return DataTransformer(config)

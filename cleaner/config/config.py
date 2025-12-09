# Configuration Management
"""
Configuration class and utilities for the data_cleaner package.
"""

import json
import os
from typing import Any, Dict, List, Optional, Union

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file.
    
    Args:
        file_path (str): Path to JSON file.
        
    Returns:
        Dict[str, Any]: Loaded JSON data.
    """
    with open(file_path, "r") as f:
        return json.load(f)

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data (Dict[str, Any]): Data to save.
        file_path (str): Path to save JSON file.
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Default configuration
DEFAULT_CONFIG = {
    "general": {
        "encoding": "utf-8",
        "logging_level": "INFO",
        "log_file": "data_cleaner.log"
    },
    "cleaners": {
        "text": {
            "remove_special_chars": True,
            "convert_case": "none",  # none, upper, lower, title
            "trim_whitespace": True,
            "max_length": None,
            "allowed_chars": None
        },
        "number": {
            "remove_formatting": True,
            "convert_to_type": "float",  # none, int, float
            "min_value": None,
            "max_value": None
        },
        "datetime": {
            "input_format": None,  # None = auto-detect
            "output_format": "%Y-%m-%d %H:%M:%S",
            "timezone": "UTC",
            "allow_future": True,
            "allow_past": True
        },
        "email": {
            "allow_subdomains": True,
            "max_length": 254,
            "allow_special_chars": True
        },
        "url": {
            "add_protocol": True,
            "default_protocol": "https",
            "remove_www": True,
            "validate_domain": True
        }
    },
    "transformers": {
        "text": {
            "tokenize": True,
            "remove_stopwords": False,
            "stemming": False,
            "lemmatization": False,
            "lowercase": True
        },
        "number": {
            "normalization": "none",  # none, min_max, z_score
            "scaling": None,
            "binning": None
        },
        "datetime": {
            "extract_parts": False,
            "extract_year": True,
            "extract_month": True,
            "extract_day": True,
            "extract_hour": False,
            "extract_minute": False,
            "extract_second": False
        },
        "categorical": {
            "encoding": "none",  # none, label, one_hot, frequency
            "handle_unknown": "ignore"
        }
    },
    "utils": {
        "data_io": {
            "chunk_size": 10000,
            "compression": None
        },
        "reporting": {
            "format": "json",  # json, csv, html
            "include_statistics": True,
            "include_summary": True
        }
    }
}

class Config:
    """
    Configuration class for managing data_cleaner settings.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a new Config instance.
        
        Args:
            config (Dict[str, Any], optional): Initial configuration.
        """
        self._config = DEFAULT_CONFIG.copy()
        
        # Merge with provided config if any
        if config:
            self.merge(config)
    
    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value using dictionary-like access.
        
        Args:
            key (str): Configuration key (supports dot notation).
            
        Returns:
            Any: Configuration value.
            
        Raises:
            KeyError: If key is not found.
        """
        return self.get(key, default=KeyError)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dictionary-like access.
        
        Args:
            key (str): Configuration key (supports dot notation).
            value (Any): Configuration value.
        """
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        
        Args:
            key (str): Configuration key (supports dot notation).
            
        Returns:
            bool: True if key exists, False otherwise.
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value with optional default.
        
        Args:
            key (str): Configuration key (supports dot notation).
            default (Any, optional): Default value if key is not found.
            
        Returns:
            Any: Configuration value or default.
        """
        keys = key.split(".")
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if default is KeyError:
                raise KeyError(f"Configuration key not found: {key}")
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key (str): Configuration key (supports dot notation).
            value (Any): Configuration value.
        """
        keys = key.split(".")
        config = self._config
        
        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def merge(self, other: Union[Dict[str, Any], "Config"]) -> None:
        """
        Merge another configuration into this one.
        
        Args:
            other (Union[Dict[str, Any], Config]): Configuration to merge.
        """
        if isinstance(other, Config):
            other_config = other._config
        else:
            other_config = other
        
        self._merge_dicts(self._config, other_config)
    
    def _merge_dicts(self, base: Dict[str, Any], other: Dict[str, Any]) -> None:
        """
        Recursively merge two dictionaries.
        
        Args:
            base (Dict[str, Any]): Base dictionary to merge into.
            other (Dict[str, Any]): Dictionary to merge from.
        """
        for key, value in other.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # Recursively merge dictionaries
                self._merge_dicts(base[key], value)
            else:
                # Override or add new key
                base[key] = value
    
    def update(self, **kwargs) -> None:
        """
        Update configuration with keyword arguments.
        
        Args:
            **kwargs: Configuration key-value pairs.
        """
        for key, value in kwargs.items():
            self.set(key, value)
    
    def reset(self, key: Optional[str] = None) -> None:
        """
        Reset configuration to default values.
        
        Args:
            key (str, optional): Specific key to reset. If None, reset entire configuration.
        """
        if key is None:
            # Reset entire configuration
            self._config = DEFAULT_CONFIG.copy()
        else:
            # Reset specific key
            keys = key.split(".")
            default_config = DEFAULT_CONFIG
            config = self._config
            
            # Navigate to the parent of the final key
            for k in keys[:-1]:
                if k not in default_config:
                    return  # Key not in default config, do nothing
                default_config = default_config[k]
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Reset the value
            final_key = keys[-1]
            if final_key in default_config:
                config[final_key] = default_config[final_key]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as a dictionary.
        """
        return self._config.copy()
    
    def __str__(self) -> str:
        """
        String representation of the configuration.
        
        Returns:
            str: String representation.
        """
        return json.dumps(self._config, indent=4)
    
    def __repr__(self) -> str:
        """
        Official representation of the configuration.
        
        Returns:
            str: Official representation.
        """
        return f"Config({json.dumps(self._config)})"

def load_config(file_path: str) -> Config:
    """
    Load configuration from a file.
    
    Args:
        file_path (str): Path to configuration file.
        
    Returns:
        Config: Loaded configuration.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    # Determine file type based on extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == ".json":
        config_data = load_json_file(file_path)
    else:
        raise ValueError(f"Unsupported configuration file format: {ext}")
    
    return Config(config_data)

def save_config(config: Config, file_path: str) -> None:
    """
    Save configuration to a file.
    
    Args:
        config (Config): Configuration to save.
        file_path (str): Path to save configuration file.
    """
    # Determine file type based on extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    config_data = config.to_dict()
    
    if ext == ".json":
        save_json_file(config_data, file_path)
    else:
        raise ValueError(f"Unsupported configuration file format: {ext}")

def merge_configs(*configs: Union[Config, Dict[str, Any]]) -> Config:
    """
    Merge multiple configurations into one.
    
    Args:
        *configs: Config objects or dictionaries to merge.
        
    Returns:
        Config: Merged configuration.
    """
    merged = Config()
    
    for config in configs:
        merged.merge(config)
    
    return merged

def create_config_from_dict(config_dict: Dict[str, Any]) -> Config:
    """
    Create a Config object from a dictionary.
    
    Args:
        config_dict (Dict[str, Any]): Configuration dictionary.
        
    Returns:
        Config: Config object.
    """
    return Config(config_dict)

def validate_config(config: Config) -> Dict[str, Any]:
    """
    Validate a configuration object.
    
    Args:
        config (Config): Configuration to validate.
        
    Returns:
        Dict[str, Any]: Validation results including:
            - valid: bool indicating if configuration is valid
            - errors: list of validation errors
            - warnings: list of validation warnings
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate general settings
    logging_level = config.get("general.logging_level")
    if logging_level and logging_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        results["warnings"].append(f"Invalid logging level: {logging_level}")
    
    # Validate text cleaner settings
    convert_case = config.get("cleaners.text.convert_case")
    if convert_case and convert_case not in ["none", "upper", "lower", "title"]:
        results["errors"].append(f"Invalid convert_case value: {convert_case}")
        results["valid"] = False
    
    # Validate number cleaner settings
    convert_to_type = config.get("cleaners.number.convert_to_type")
    if convert_to_type and convert_to_type not in ["none", "int", "float"]:
        results["errors"].append(f"Invalid convert_to_type value: {convert_to_type}")
        results["valid"] = False
    
    # Validate datetime cleaner settings
    output_format = config.get("cleaners.datetime.output_format")
    if not output_format:
        results["errors"].append("Missing datetime output_format")
        results["valid"] = False
    
    # Validate email cleaner settings
    max_length = config.get("cleaners.email.max_length")
    if max_length and (not isinstance(max_length, int) or max_length <= 0):
        results["errors"].append(f"Invalid email max_length: {max_length}")
        results["valid"] = False
    
    # Validate URL cleaner settings
    default_protocol = config.get("cleaners.url.default_protocol")
    if default_protocol and default_protocol not in ["http", "https"]:
        results["warnings"].append(f"Unusual default_protocol: {default_protocol}")
    
    return results

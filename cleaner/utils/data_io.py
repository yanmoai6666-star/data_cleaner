# Data IO Utilities
"""
Functions for loading and saving data in various formats.
"""

import os
import json
import csv
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ..config import Config

# Default encoding
DEFAULT_ENCODING = "utf-8"

def load_data(file_path: str, config: Optional[Config] = None, **kwargs) -> Union[pd.DataFrame, List, Dict]:
    """
    Load data from a file.
    
    Args:
        file_path (str): Path to the file.
        config (Config, optional): Configuration object with loading parameters.
        **kwargs: Additional parameters to pass to the loading function.
        
    Returns:
        Union[pd.DataFrame, List, Dict]: Loaded data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    # Get default configuration
    encoding = kwargs.get("encoding", DEFAULT_ENCODING)
    
    if config:
        # Override with config if provided
        encoding = config.get("data_io.encoding", encoding)
    
    # Load based on file extension
    if extension == ".csv":
        return load_csv(file_path, encoding=encoding, **kwargs)
        
    elif extension == ".json":
        return load_json(file_path, encoding=encoding, **kwargs)
        
    elif extension in [".xlsx", ".xls"]:
        return load_excel(file_path, **kwargs)
        
    elif extension == ".txt":
        return load_text(file_path, encoding=encoding, **kwargs)
        
    elif extension == ".parquet":
        return load_parquet(file_path, **kwargs)
        
    else:
        raise ValueError(f"Unsupported file format: {extension}")

def save_data(data: Any, file_path: str, config: Optional[Config] = None, **kwargs) -> None:
    """
    Save data to a file.
    
    Args:
        data (Any): Data to save.
        file_path (str): Path to save the file.
        config (Config, optional): Configuration object with saving parameters.
        **kwargs: Additional parameters to pass to the saving function.
        
    Raises:
        ValueError: If the file format is not supported or data type is not compatible.
    """
    # Get file extension
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    # Get default configuration
    encoding = kwargs.get("encoding", DEFAULT_ENCODING)
    
    if config:
        # Override with config if provided
        encoding = config.get("data_io.encoding", encoding)
    
    # Save based on file extension
    if extension == ".csv":
        save_csv(data, file_path, encoding=encoding, **kwargs)
        
    elif extension == ".json":
        save_json(data, file_path, encoding=encoding, **kwargs)
        
    elif extension in [".xlsx", ".xls"]:
        save_excel(data, file_path, **kwargs)
        
    elif extension == ".txt":
        save_text(data, file_path, encoding=encoding, **kwargs)
        
    elif extension == ".parquet":
        save_parquet(data, file_path, **kwargs)
        
    else:
        raise ValueError(f"Unsupported file format: {extension}")

def load_csv(file_path: str, encoding: str = DEFAULT_ENCODING, **kwargs) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        encoding (str): File encoding.
        **kwargs: Additional parameters to pass to pandas.read_csv.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    return pd.read_csv(file_path, encoding=encoding, **kwargs)

def save_csv(data: Union[pd.DataFrame, List[Dict]], file_path: str, encoding: str = DEFAULT_ENCODING, **kwargs) -> None:
    """
    Save data to a CSV file.
    
    Args:
        data (Union[pd.DataFrame, List[Dict]]): Data to save.
        file_path (str): Path to save the CSV file.
        encoding (str): File encoding.
        **kwargs: Additional parameters to pass to pandas.to_csv or csv.writer.
        
    Raises:
        ValueError: If data type is not supported.
    """
    if isinstance(data, pd.DataFrame):
        data.to_csv(file_path, encoding=encoding, **kwargs)
    elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
        with open(file_path, "w", encoding=encoding, newline="") as f:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames, **kwargs)
                writer.writeheader()
                writer.writerows(data)
    else:
        raise ValueError("Data must be a pandas DataFrame or a list of dictionaries")

def load_json(file_path: str, encoding: str = DEFAULT_ENCODING, **kwargs) -> Union[List, Dict]:
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
        encoding (str): File encoding.
        **kwargs: Additional parameters to pass to json.load.
        
    Returns:
        Union[List, Dict]: Loaded JSON data.
    """
    with open(file_path, "r", encoding=encoding) as f:
        return json.load(f, **kwargs)

def save_json(data: Any, file_path: str, encoding: str = DEFAULT_ENCODING, indent: int = 4, **kwargs) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data (Any): Data to save (must be JSON serializable).
        file_path (str): Path to save the JSON file.
        encoding (str): File encoding.
        indent (int): Number of spaces for indentation.
        **kwargs: Additional parameters to pass to json.dump.
    """
    with open(file_path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=indent, **kwargs)

def load_excel(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Load data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file.
        **kwargs: Additional parameters to pass to pandas.read_excel.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    return pd.read_excel(file_path, **kwargs)

def save_excel(data: pd.DataFrame, file_path: str, **kwargs) -> None:
    """
    Save data to an Excel file.
    
    Args:
        data (pd.DataFrame): Data to save.
        file_path (str): Path to save the Excel file.
        **kwargs: Additional parameters to pass to pandas.to_excel.
    """
    with pd.ExcelWriter(file_path) as writer:
        data.to_excel(writer, **kwargs)

def load_text(file_path: str, encoding: str = DEFAULT_ENCODING, **kwargs) -> List[str]:
    """
    Load data from a text file.
    
    Args:
        file_path (str): Path to the text file.
        encoding (str): File encoding.
        **kwargs: Additional parameters to pass to open.
        
    Returns:
        List[str]: List of lines from the file.
    """
    with open(file_path, "r", encoding=encoding, **kwargs) as f:
        return f.readlines()

def save_text(data: Union[str, List[str]], file_path: str, encoding: str = DEFAULT_ENCODING, **kwargs) -> None:
    """
    Save data to a text file.
    
    Args:
        data (Union[str, List[str]]): Data to save (string or list of strings).
        file_path (str): Path to save the text file.
        encoding (str): File encoding.
        **kwargs: Additional parameters to pass to open.
    """
    with open(file_path, "w", encoding=encoding, **kwargs) as f:
        if isinstance(data, list):
            f.writelines(data)
        else:
            f.write(data)

def load_parquet(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Load data from a Parquet file.
    
    Args:
        file_path (str): Path to the Parquet file.
        **kwargs: Additional parameters to pass to pandas.read_parquet.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    return pd.read_parquet(file_path, **kwargs)

def save_parquet(data: pd.DataFrame, file_path: str, **kwargs) -> None:
    """
    Save data to a Parquet file.
    
    Args:
        data (pd.DataFrame): Data to save.
        file_path (str): Path to save the Parquet file.
        **kwargs: Additional parameters to pass to pandas.to_parquet.
    """
    data.to_parquet(file_path, **kwargs)

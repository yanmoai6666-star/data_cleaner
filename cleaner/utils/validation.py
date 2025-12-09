# Validation Utilities
"""
Functions for validating data quality and formats.
"""

import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

def validate_data(data: Any, schema: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
    """
    Validate data against a schema.
    
    Args:
        data (Any): Data to validate.
        schema (Dict, optional): Validation schema.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Validation results including:
            - valid: bool indicating if data is valid
            - errors: list of error messages
            - warnings: list of warning messages
            - validated_data: cleaned/validated data if applicable
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "validated_data": data
    }
    
    if not schema:
        # If no schema provided, perform basic validation
        return validate_basic(data, results, **kwargs)
    
    # Perform schema-based validation
    validation_type = schema.get("type", "")
    
    if validation_type == "string":
        return validate_string(data, schema, results, **kwargs)
        
    elif validation_type == "number":
        return validate_number(data, schema, results, **kwargs)
        
    elif validation_type == "integer":
        return validate_integer(data, schema, results, **kwargs)
        
    elif validation_type == "boolean":
        return validate_boolean(data, schema, results, **kwargs)
        
    elif validation_type == "datetime":
        return validate_datetime(data, schema, results, **kwargs)
        
    elif validation_type == "list":
        return validate_list(data, schema, results, **kwargs)
        
    elif validation_type == "dict":
        return validate_dict(data, schema, results, **kwargs)
        
    elif validation_type == "email":
        return validate_email(data, schema, results, **kwargs)
        
    elif validation_type == "url":
        return validate_url(data, schema, results, **kwargs)
        
    else:
        results["errors"].append(f"Unsupported validation type: {validation_type}")
        results["valid"] = False
        return results

def validate_basic(data: Any, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Perform basic validation checks.
    
    Args:
        data (Any): Data to validate.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    # Check for None/NaN if not allowed
    allow_null = kwargs.get("allow_null", False)
    
    if data is None:
        if not allow_null:
            results["errors"].append("Value cannot be None")
            results["valid"] = False
    elif hasattr(data, "__iter__") and not isinstance(data, (str, bytes)):
        # Check empty collections
        allow_empty = kwargs.get("allow_empty", False)
        if len(data) == 0 and not allow_empty:
            results["errors"].append("Collection cannot be empty")
            results["valid"] = False
    
    return results

def validate_string(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate string data.
    
    Args:
        data (Any): Data to validate.
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    if not isinstance(data, str):
        results["errors"].append(f"Expected string, got {type(data).__name__}")
        results["valid"] = False
        return results
    
    # Length validation
    min_length = schema.get("min_length", 0)
    max_length = schema.get("max_length", None)
    
    if len(data) < min_length:
        results["errors"].append(f"String must be at least {min_length} characters long")
        results["valid"] = False
        
    if max_length is not None and len(data) > max_length:
        results["errors"].append(f"String must be at most {max_length} characters long")
        results["valid"] = False
    
    # Pattern validation
    pattern = schema.get("pattern", None)
    if pattern:
        if not re.match(pattern, data):
            results["errors"].append(f"String must match pattern: {pattern}")
            results["valid"] = False
    
    # Choice validation
    choices = schema.get("choices", None)
    if choices and data not in choices:
        results["errors"].append(f"String must be one of: {', '.join(choices)}")
        results["valid"] = False
    
    # Case validation
    case = schema.get("case", None)
    if case == "upper" and not data.isupper():
        results["warnings"].append("String should be uppercase")
    elif case == "lower" and not data.islower():
        results["warnings"].append("String should be lowercase")
    
    return results

def validate_number(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate numeric data.
    
    Args:
        data (Any): Data to validate.
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    if not isinstance(data, (int, float)):
        results["errors"].append(f"Expected number, got {type(data).__name__}")
        results["valid"] = False
        return results
    
    # Range validation
    minimum = schema.get("minimum", None)
    maximum = schema.get("maximum", None)
    
    if minimum is not None and data < minimum:
        results["errors"].append(f"Number must be at least {minimum}")
        results["valid"] = False
        
    if maximum is not None and data > maximum:
        results["errors"].append(f"Number must be at most {maximum}")
        results["valid"] = False
    
    # Multiple validation
    multiple_of = schema.get("multiple_of", None)
    if multiple_of is not None and data % multiple_of != 0:
        results["errors"].append(f"Number must be a multiple of {multiple_of}")
        results["valid"] = False
    
    return results

def validate_integer(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate integer data.
    
    Args:
        data (Any): Data to validate.
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    if not isinstance(data, int):
        results["errors"].append(f"Expected integer, got {type(data).__name__}")
        results["valid"] = False
        return results
    
    # Use number validation for range checks
    return validate_number(data, schema, results, **kwargs)

def validate_boolean(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate boolean data.
    
    Args:
        data (Any): Data to validate.
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    if not isinstance(data, bool):
        results["errors"].append(f"Expected boolean, got {type(data).__name__}")
        results["valid"] = False
    
    return results

def validate_datetime(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate datetime data.
    
    Args:
        data (Any): Data to validate (datetime object or string).
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    # Parse string to datetime if needed
    if isinstance(data, str):
        date_format = schema.get("format", None)
        try:
            if date_format:
                data = datetime.strptime(data, date_format)
            else:
                data = datetime.fromisoformat(data)
        except (ValueError, TypeError):
            results["errors"].append(f"Invalid datetime format: {data}")
            results["valid"] = False
            return results
    elif not isinstance(data, datetime):
        results["errors"].append(f"Expected datetime object or string, got {type(data).__name__}")
        results["valid"] = False
        return results
    
    # Date range validation
    min_date = schema.get("min_date", None)
    max_date = schema.get("max_date", None)
    
    if min_date and data < min_date:
        results["errors"].append(f"Date must be on or after {min_date}")
        results["valid"] = False
        
    if max_date and data > max_date:
        results["errors"].append(f"Date must be on or before {max_date}")
        results["valid"] = False
    
    results["validated_data"] = data
    return results

def validate_list(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate list data.
    
    Args:
        data (Any): Data to validate.
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    if not isinstance(data, list):
        results["errors"].append(f"Expected list, got {type(data).__name__}")
        results["valid"] = False
        return results
    
    # Length validation
    min_items = schema.get("min_items", 0)
    max_items = schema.get("max_items", None)
    
    if len(data) < min_items:
        results["errors"].append(f"List must contain at least {min_items} items")
        results["valid"] = False
        
    if max_items is not None and len(data) > max_items:
        results["errors"].append(f"List must contain at most {max_items} items")
        results["valid"] = False
    
    # Item validation
    item_schema = schema.get("items", None)
    if item_schema:
        validated_items = []
        for i, item in enumerate(data):
            item_result = validate_data(item, item_schema, **kwargs)
            if not item_result["valid"]:
                for error in item_result["errors"]:
                    results["errors"].append(f"Item {i}: {error}")
                results["valid"] = False
            validated_items.append(item_result["validated_data"])
        results["validated_data"] = validated_items
    
    return results

def validate_dict(data: Any, schema: Dict, results: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Validate dictionary data.
    
    Args:
        data (Any): Data to validate.
        schema (Dict): Validation schema.
        results (Dict): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Updated results dictionary.
    """
    if not isinstance(data, dict):
        results["errors"].append(f"Expected dictionary, got {type(data).__name__}")
        results["valid"] = False
        return results
    
    # Properties validation
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    # Check required fields
    for field in required:
        if field not in data:
            results["errors"].append(f"Required field missing: {field}")
            results["valid"] = False
    
    # Validate properties
    validated_data = {}
    for field, field_schema in properties.items():
        if field in data:
            field_result = validate_data(data[field], field_schema, **kwargs)
            if not field_result["valid"]:
                for error in field_result["errors"]:
                    results["errors"].append(f"Field '{field}': {error}")
                results["valid"] = False
            validated_data[field] = field_result["validated_data"]
        elif field not in required:
            # Optional field not provided
            pass
    
    results["validated_data"] = validated_data
    return results

def validate_email(email: str, schema: Optional[Dict] = None, results: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
    """
    Validate email address format.
    
    Args:
        email (str): Email address to validate.
        schema (Dict, optional): Validation schema.
        results (Dict, optional): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Validation results.
    """
    if results is None:
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "validated_data": email
        }
    
    if not isinstance(email, str):
        results["errors"].append(f"Expected string, got {type(email).__name__}")
        results["valid"] = False
        return results
    
    # Email regex pattern
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if schema and "pattern" in schema:
        email_pattern = schema["pattern"]
    
    if not re.match(email_pattern, email):
        results["errors"].append(f"Invalid email format: {email}")
        results["valid"] = False
    
    # Additional email validation options
    max_length = kwargs.get("max_length", 254)  # RFC 5321 limit
    if len(email) > max_length:
        results["errors"].append(f"Email exceeds maximum length of {max_length} characters")
        results["valid"] = False
    
    return results

def validate_url(url: str, schema: Optional[Dict] = None, results: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
    """
    Validate URL format.
    
    Args:
        url (str): URL to validate.
        schema (Dict, optional): Validation schema.
        results (Dict, optional): Results dictionary to update.
        **kwargs: Additional validation parameters.
        
    Returns:
        Dict[str, Any]: Validation results.
    """
    if results is None:
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "validated_data": url
        }
    
    if not isinstance(url, str):
        results["errors"].append(f"Expected string, got {type(url).__name__}")
        results["valid"] = False
        return results
    
    # URL regex pattern (simplified)
    url_pattern = r"^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$"
    
    if schema and "pattern" in schema:
        url_pattern = schema["pattern"]
    
    if not re.match(url_pattern, url):
        results["errors"].append(f"Invalid URL format: {url}")
        results["valid"] = False
    
    return results

def is_valid_type(value: Any, expected_type: Union[type, tuple]) -> bool:
    """
    Check if value is of expected type.
    
    Args:
        value (Any): Value to check.
        expected_type (Union[type, tuple]): Expected type or tuple of types.
        
    Returns:
        bool: True if value is of expected type, False otherwise.
    """
    return isinstance(value, expected_type)

def is_in_range(value: Union[int, float], min_val: Optional[Union[int, float]] = None, 
                max_val: Optional[Union[int, float]] = None) -> bool:
    """
    Check if value is within specified range.
    
    Args:
        value (Union[int, float]): Value to check.
        min_val (Union[int, float], optional): Minimum allowed value.
        max_val (Union[int, float], optional): Maximum allowed value.
        
    Returns:
        bool: True if value is in range, False otherwise.
    """
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True

# Reporting Utilities
"""
Functions for generating data cleaning and transformation reports.
"""

import json
import pandas as pd
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

def generate_report(data: Any, report_type: str = "cleaning", **kwargs) -> Dict[str, Any]:
    """
    Generate a report for data processing operations.
    
    Args:
        data (Any): Data to generate report for.
        report_type (str): Type of report to generate (cleaning, transformation, quality).
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: Generated report with metadata and results.
    """
    # Create base report structure
    report = {
        "report_type": report_type,
        "generated_at": datetime.now().isoformat(),
        "metadata": {
            "data_type": type(data).__name__
        },
        "results": {},
        "statistics": {},
        "summary": {}
    }
    
    # Generate report based on type
    if report_type == "cleaning":
        return generate_cleaning_report(data, report, **kwargs)
        
    elif report_type == "transformation":
        return generate_transformation_report(data, report, **kwargs)
        
    elif report_type == "quality":
        return generate_quality_report(data, report, **kwargs)
        
    elif report_type == "validation":
        return generate_validation_report(data, report, **kwargs)
        
    else:
        report["errors"] = [f"Unsupported report type: {report_type}"]
        return report

def generate_cleaning_report(data: Any, report: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Generate a data cleaning report.
    
    Args:
        data (Any): Cleaned data or cleaning results.
        report (Dict): Base report structure.
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: Cleaning report.
    """
    # Extract cleaning results if available
    if isinstance(data, dict) and "cleaning_results" in data:
        cleaning_results = data["cleaning_results"]
        original_data = data.get("original_data")
        cleaned_data = data.get("cleaned_data")
    else:
        cleaning_results = data
        original_data = kwargs.get("original_data")
        cleaned_data = kwargs.get("cleaned_data")
    
    # Add cleaning results
    report["results"] = {
        "total_records": cleaning_results.get("total_records", 0),
        "cleaned_records": cleaning_results.get("cleaned_records", 0),
        "failed_records": cleaning_results.get("failed_records", 0),
        "cleaned_fields": cleaning_results.get("cleaned_fields", {}),
        "cleaning_operations": cleaning_results.get("cleaning_operations", []),
        "errors": cleaning_results.get("errors", []),
        "warnings": cleaning_results.get("warnings", [])
    }
    
    # Calculate statistics
    if original_data is not None and cleaned_data is not None:
        report["statistics"] = calculate_cleaning_statistics(original_data, cleaned_data)
    
    # Generate summary
    report["summary"] = {
        "cleaning_success_rate": calculate_success_rate(report["results"]),
        "most_common_operations": get_most_common_operations(report["results"]),
        "total_cleaning_time": kwargs.get("total_time", 0)
    }
    
    return report

def generate_transformation_report(data: Any, report: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Generate a data transformation report.
    
    Args:
        data (Any): Transformed data or transformation results.
        report (Dict): Base report structure.
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: Transformation report.
    """
    # Extract transformation results if available
    if isinstance(data, dict) and "transformation_results" in data:
        transformation_results = data["transformation_results"]
        original_data = data.get("original_data")
        transformed_data = data.get("transformed_data")
    else:
        transformation_results = data
        original_data = kwargs.get("original_data")
        transformed_data = kwargs.get("transformed_data")
    
    # Add transformation results
    report["results"] = {
        "total_records": transformation_results.get("total_records", 0),
        "transformed_records": transformation_results.get("transformed_records", 0),
        "failed_records": transformation_results.get("failed_records", 0),
        "transformed_fields": transformation_results.get("transformed_fields", {}),
        "transformation_operations": transformation_results.get("transformation_operations", []),
        "errors": transformation_results.get("errors", []),
        "warnings": transformation_results.get("warnings", [])
    }
    
    # Calculate statistics
    if original_data is not None and transformed_data is not None:
        report["statistics"] = calculate_transformation_statistics(original_data, transformed_data)
    
    # Generate summary
    report["summary"] = {
        "transformation_success_rate": calculate_success_rate(report["results"]),
        "most_common_operations": get_most_common_operations(report["results"]),
        "total_transformation_time": kwargs.get("total_time", 0)
    }
    
    return report

def generate_quality_report(data: Any, report: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Generate a data quality report.
    
    Args:
        data (Any): Data to assess quality for.
        report (Dict): Base report structure.
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: Data quality report.
    """
    # Check if data is a pandas DataFrame
    if isinstance(data, pd.DataFrame):
        return generate_dataframe_quality_report(data, report, **kwargs)
    
    # For other data types
    report["results"] = {
        "data_type": type(data).__name__,
        "data_size": get_data_size(data),
        "missing_values": count_missing_values(data)
    }
    
    # Generate summary
    report["summary"] = {
        "quality_score": calculate_quality_score(report["results"])
    }
    
    return report

def generate_dataframe_quality_report(df: pd.DataFrame, report: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Generate a data quality report for a pandas DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to assess quality for.
        report (Dict): Base report structure.
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: DataFrame quality report.
    """
    # Update metadata
    report["metadata"].update({
        "rows": len(df),
        "columns": len(df.columns),
        "columns_list": list(df.columns)
    })
    
    # Calculate column-wise statistics
    column_stats = {}
    for column in df.columns:
        column_stats[column] = {
            "data_type": str(df[column].dtype),
            "count": df[column].count(),
            "missing_count": df[column].isna().sum(),
            "missing_percentage": (df[column].isna().sum() / len(df) * 100) if len(df) > 0 else 0,
            "unique_count": df[column].nunique(),
            "unique_percentage": (df[column].nunique() / len(df) * 100) if len(df) > 0 else 0
        }
        
        # Add numeric statistics if applicable
        if pd.api.types.is_numeric_dtype(df[column]):
            column_stats[column].update({
                "min": df[column].min(),
                "max": df[column].max(),
                "mean": df[column].mean(),
                "median": df[column].median(),
                "std": df[column].std(),
                "variance": df[column].var()
            })
        
        # Add string statistics if applicable
        elif pd.api.types.is_string_dtype(df[column]):
            column_stats[column].update({
                "min_length": df[column].str.len().min(),
                "max_length": df[column].str.len().max(),
                "mean_length": df[column].str.len().mean()
            })
    
    # Add results
    report["results"] = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "total_missing_values": df.isna().sum().sum(),
        "total_missing_percentage": (df.isna().sum().sum() / df.size * 100) if df.size > 0 else 0,
        "columns_statistics": column_stats,
        "duplicate_rows": df.duplicated().sum(),
        "duplicate_rows_percentage": (df.duplicated().sum() / len(df) * 100) if len(df) > 0 else 0
    }
    
    # Calculate overall statistics
    report["statistics"] = {
        "numeric_columns": sum(1 for col in df.columns if pd.api.types.is_numeric_dtype(df[col])),
        "string_columns": sum(1 for col in df.columns if pd.api.types.is_string_dtype(df[col])),
        "datetime_columns": sum(1 for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])),
        "object_columns": sum(1 for col in df.columns if pd.api.types.is_object_dtype(df[col])),
        "columns_with_missing_values": sum(1 for col_stats in column_stats.values() if col_stats["missing_count"] > 0),
        "columns_with_high_missing_values": sum(1 for col_stats in column_stats.values() if col_stats["missing_percentage"] > 50)
    }
    
    # Generate summary
    report["summary"] = {
        "quality_score": calculate_quality_score(report["results"]),
        "most_complete_columns": get_most_complete_columns(column_stats, top_n=5),
        "most_incomplete_columns": get_most_incomplete_columns(column_stats, top_n=5),
        "most_duplicated_columns": get_most_duplicated_columns(df, top_n=5)
    }
    
    return report

def generate_validation_report(data: Any, report: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Generate a data validation report.
    
    Args:
        data (Any): Validation results or data to validate.
        report (Dict): Base report structure.
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: Validation report.
    """
    # Extract validation results if available
    if isinstance(data, dict) and "validation_results" in data:
        validation_results = data["validation_results"]
    else:
        validation_results = data
    
    # Add validation results
    report["results"] = {
        "valid_records": validation_results.get("valid", 0),
        "invalid_records": validation_results.get("invalid", 0),
        "validation_errors": validation_results.get("errors", []),
        "validation_warnings": validation_results.get("warnings", []),
        "validation_rules": kwargs.get("validation_rules", [])
    }
    
    # Generate summary
    report["summary"] = {
        "validation_success_rate": calculate_validation_success_rate(report["results"]),
        "most_common_errors": get_most_common_errors(report["results"]),
        "validation_coverage": kwargs.get("validation_coverage", 0)
    }
    
    return report

def calculate_cleaning_statistics(original_data: Any, cleaned_data: Any) -> Dict[str, Any]:
    """
    Calculate statistics for data cleaning operations.
    
    Args:
        original_data (Any): Original data before cleaning.
        cleaned_data (Any): Data after cleaning.
        
    Returns:
        Dict[str, Any]: Cleaning statistics.
    """
    stats = {}
    
    # Handle pandas DataFrames
    if isinstance(original_data, pd.DataFrame) and isinstance(cleaned_data, pd.DataFrame):
        stats["rows_removed"] = len(original_data) - len(cleaned_data)
        stats["columns_modified"] = sum(1 for col in original_data.columns if not original_data[col].equals(cleaned_data[col]))
        stats["total_changes"] = original_data.ne(cleaned_data).sum().sum()
    
    return stats

def calculate_transformation_statistics(original_data: Any, transformed_data: Any) -> Dict[str, Any]:
    """
    Calculate statistics for data transformation operations.
    
    Args:
        original_data (Any): Original data before transformation.
        transformed_data (Any): Data after transformation.
        
    Returns:
        Dict[str, Any]: Transformation statistics.
    """
    stats = {}
    
    # Handle pandas DataFrames
    if isinstance(original_data, pd.DataFrame) and isinstance(transformed_data, pd.DataFrame):
        stats["rows_changed"] = len(original_data)
        stats["columns_added"] = len(transformed_data.columns) - len(original_data.columns)
        stats["columns_removed"] = len(original_data.columns) - len(transformed_data.columns)
        stats["columns_modified"] = sum(1 for col in original_data.columns if col in transformed_data.columns and not original_data[col].equals(transformed_data[col]))
    
    return stats

def calculate_success_rate(results: Dict[str, Any]) -> float:
    """
    Calculate the success rate of data operations.
    
    Args:
        results (Dict): Operation results.
        
    Returns:
        float: Success rate as a percentage.
    """
    total = results.get("total_records", 0)
    if total == 0:
        return 0.0
    
    if "cleaned_records" in results:
        success = results["cleaned_records"]
    elif "transformed_records" in results:
        success = results["transformed_records"]
    else:
        return 0.0
    
    return (success / total) * 100

def calculate_validation_success_rate(results: Dict[str, Any]) -> float:
    """
    Calculate the validation success rate.
    
    Args:
        results (Dict): Validation results.
        
    Returns:
        float: Validation success rate as a percentage.
    """
    valid = results.get("valid_records", 0)
    invalid = results.get("invalid_records", 0)
    total = valid + invalid
    
    if total == 0:
        return 0.0
    
    return (valid / total) * 100

def calculate_quality_score(results: Dict[str, Any]) -> float:
    """
    Calculate a quality score for the data.
    
    Args:
        results (Dict): Data quality results.
        
    Returns:
        float: Quality score (0-100).
    """
    score = 100.0
    
    # Subtract points for missing values
    missing_percentage = results.get("total_missing_percentage", 0)
    score -= missing_percentage
    
    # Subtract points for duplicate rows
    duplicate_percentage = results.get("duplicate_rows_percentage", 0)
    score -= duplicate_percentage * 0.5  # Duplicates are less severe than missing values
    
    # Ensure score is between 0 and 100
    return max(0.0, min(100.0, score))

def get_data_size(data: Any) -> int:
    """
    Get the size of the data.
    
    Args:
        data (Any): Data to get size for.
        
    Returns:
        int: Size of the data.
    """
    if isinstance(data, (list, tuple, set)):
        return len(data)
    elif isinstance(data, dict):
        return len(data)
    elif isinstance(data, str):
        return len(data)
    elif isinstance(data, pd.DataFrame):
        return data.size
    elif isinstance(data, pd.Series):
        return len(data)
    else:
        return 0

def count_missing_values(data: Any) -> int:
    """
    Count missing values in the data.
    
    Args:
        data (Any): Data to count missing values for.
        
    Returns:
        int: Number of missing values.
    """
    if isinstance(data, pd.DataFrame):
        return data.isna().sum().sum()
    elif isinstance(data, pd.Series):
        return data.isna().sum()
    elif isinstance(data, (list, tuple)):
        return sum(1 for x in data if x is None or pd.isna(x))
    elif isinstance(data, dict):
        return sum(1 for x in data.values() if x is None or pd.isna(x))
    else:
        return 0

def get_most_common_operations(results: Dict[str, Any]) -> List[str]:
    """
    Get the most common cleaning/transformation operations.
    
    Args:
        results (Dict): Operation results.
        
    Returns:
        List[str]: Most common operations.
    """
    operations = results.get("cleaning_operations", []) or results.get("transformation_operations", [])
    
    if not operations:
        return []
    
    # Count operation frequencies
    operation_counts = {}
    for op in operations:
        op_name = op.get("name", "unknown")
        operation_counts[op_name] = operation_counts.get(op_name, 0) + 1
    
    # Sort by frequency
    sorted_operations = sorted(operation_counts.items(), key=lambda x: x[1], reverse=True)
    return [op[0] for op in sorted_operations[:5]]

def get_most_complete_columns(column_stats: Dict[str, Any], top_n: int = 5) -> List[str]:
    """
    Get the most complete columns (least missing values).
    
    Args:
        column_stats (Dict): Column statistics.
        top_n (int): Number of columns to return.
        
    Returns:
        List[str]: Most complete columns.
    """
    # Sort columns by missing percentage
    sorted_columns = sorted(column_stats.items(), key=lambda x: x[1]["missing_percentage"])
    return [col[0] for col in sorted_columns[:top_n]]

def get_most_incomplete_columns(column_stats: Dict[str, Any], top_n: int = 5) -> List[str]:
    """
    Get the most incomplete columns (most missing values).
    
    Args:
        column_stats (Dict): Column statistics.
        top_n (int): Number of columns to return.
        
    Returns:
        List[str]: Most incomplete columns.
    """
    # Sort columns by missing percentage (descending)
    sorted_columns = sorted(column_stats.items(), key=lambda x: x[1]["missing_percentage"], reverse=True)
    return [col[0] for col in sorted_columns[:top_n]]

def get_most_duplicated_columns(df: pd.DataFrame, top_n: int = 5) -> List[str]:
    """
    Get the columns with the most duplicated values.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze.
        top_n (int): Number of columns to return.
        
    Returns:
        List[str]: Most duplicated columns.
    """
    duplicate_counts = {}
    
    for column in df.columns:
        duplicate_count = df[column].duplicated().sum()
        duplicate_counts[column] = duplicate_count
    
    # Sort by duplicate count (descending)
    sorted_columns = sorted(duplicate_counts.items(), key=lambda x: x[1], reverse=True)
    return [col[0] for col in sorted_columns[:top_n]]

def get_most_common_errors(results: Dict[str, Any]) -> List[str]:
    """
    Get the most common validation errors.
    
    Args:
        results (Dict): Validation results.
        
    Returns:
        List[str]: Most common errors.
    """
    errors = results.get("validation_errors", [])
    
    if not errors:
        return []
    
    # Count error frequencies
    error_counts = {}
    for error in errors:
        error_msg = error.get("message", "unknown")
        error_counts[error_msg] = error_counts.get(error_msg, 0) + 1
    
    # Sort by frequency
    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    return [err[0] for err in sorted_errors[:5]]

def export_report(report: Dict[str, Any], file_path: str, format: str = "json", **kwargs) -> None:
    """
    Export a report to a file.
    
    Args:
        report (Dict): Report to export.
        file_path (str): File path to export to.
        format (str): Export format (json, csv, html).
        **kwargs: Additional export parameters.
    """
    if format == "json":
        with open(file_path, "w") as f:
            json.dump(report, f, indent=4, default=str)
    
    elif format == "csv" and "columns_statistics" in report.get("results", {}):
        # Export column statistics as CSV
        column_stats = report["results"]["columns_statistics"]
        df = pd.DataFrame.from_dict(column_stats, orient="index")
        df.to_csv(file_path)
    
    elif format == "html":
        # Simple HTML export
        html_content = generate_html_report(report)
        with open(file_path, "w") as f:
            f.write(html_content)

def generate_html_report(report: Dict[str, Any]) -> str:
    """
    Generate an HTML representation of a report.
    
    Args:
        report (Dict): Report to convert to HTML.
        
    Returns:
        str: HTML representation of the report.
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{report['report_type'].title()} Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .report-header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .report-section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .section-title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
            .summary-item {{ margin: 5px 0; }}
            table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f0f0f0; }}
        </style>
    </head>
    <body>
        <div class="report-header">
            <h1>{report['report_type'].title()} Report</h1>
            <p>Generated at: {report['generated_at']}</p>
        </div>
    """
    
    # Add summary section
    if "summary" in report:
        html += f"""
        <div class="report-section">
            <div class="section-title">Summary</div>
        """
        for key, value in report['summary'].items():
            if isinstance(value, list):
                value_str = ", ".join(value)
            else:
                value_str = str(value)
            html += f"<div class='summary-item'><strong>{key}:</strong> {value_str}</div>"
        html += "</div>"
    
    html += "</body></html>"
    return html

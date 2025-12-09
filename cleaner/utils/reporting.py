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
        return generate_cleaning_report(data, report,** kwargs)
        
    elif report_type == "transformation":
        return generate_transformation_report(data, report, **kwargs)
        
    elif report_type == "quality":
        return generate_quality_report(data, report,** kwargs)
        
    elif report_type == "validation":
        return generate_validation_report(data, report, **kwargs)
        
    else:
        report["errors"] = [f"Unsupported report type: {report_type}"]
        return report


def generate_cleaning_report(data: Any, report: Dict[str, Any],** kwargs) -> Dict[str, Any]:
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


def generate_transformation_report(data: Any, report: Dict[str, Any],** kwargs) -> Dict[str, Any]:
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


def generate_quality_report(data: Any, report: Dict[str, Any],** kwargs) -> Dict[str, Any]:
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
        return generate_dataframe_quality_report(data, report,** kwargs)
    
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
            
            # Calculate IQR and detect outliers
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            # Count outliers
            outliers = df[column][(df[column] < lower_bound) | (df[column] > upper_bound)]
            outlier_count = len(outliers)
            outlier_percentage = (outlier_count / len(df) * 100) if len(df) > 0 else 0
            
            # Add to column stats
            column_stats[column].update({
                "outlier_count": outlier_count,
                "outlier_percentage": outlier_percentage
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
        "duplicate_rows_percentage": (df.duplicated().sum() / len(df) * 100) if len(df) > 0 else 0,
        # Total outliers across all numeric columns
        "total_outliers": sum(col_stats["outlier_count"] for col_stats in column_stats.values() if "outlier_count" in col_stats),
        # Columns with at least one outlier
        "columns_with_outliers": [col for col, col_stats in column_stats.items() if "outlier_count" in col_stats and col_stats["outlier_count"] > 0]
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
        "most_duplicated_columns": get_most_duplicated_columns(df, top_n=5),
        # Most outlier-prone columns (top 3)
        "most_outlier_prone_columns": sorted(
            [{"column": col, "outlier_percentage": col_stats["outlier_percentage"]} 
             for col, col_stats in column_stats.items() if "outlier_percentage" in col_stats],
            key=lambda x: x["outlier_percentage"],
            reverse=True
        )[:3]
    }
    
    return report


def generate_validation_report(data: Any, report: Dict[str, Any],** kwargs) -> Dict[str, Any]:
    """
    Generate a data validation report.
    
    Args:
        data (Any): Validation results or data to validate.
        report (Dict): Base report structure.
        **kwargs: Additional report parameters.
        
    Returns:
        Dict[str, Any]: Validation report.
    """
    # (Original function implementation remains unchanged)
    pass


# The following functions are assumed to exist in the original codebase
# and are included here for completeness (their implementations may vary)
def calculate_cleaning_statistics(original_data, cleaned_data):
    return {}


def calculate_transformation_statistics(original_data, transformed_data):
    return {}


def calculate_success_rate(results):
    return 0.0


def get_most_common_operations(results):
    return []


def get_data_size(data):
    return 0


def count_missing_values(data):
    return 0


def calculate_quality_score(results):
    return 0.0


def get_most_complete_columns(column_stats, top_n=5):
    return []


def get_most_incomplete_columns(column_stats, top_n=5):
    return []


def get_most_duplicated_columns(df, top_n=5):
    return []

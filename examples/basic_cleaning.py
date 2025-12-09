#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic Data Cleaning Example

This example demonstrates how to use the data_cleaner package for basic data cleaning tasks.
"""

from data_cleaner import (
    TextCleaner,
    NumberCleaner,
    DateTimeCleaner,
    EmailCleaner,
    URLCleaner,
    Config
)
from data_cleaner.utils import generate_report


def main():
    """
    Main function to demonstrate basic data cleaning.
    """
    print("=== Data Cleaning Examples ===\n")
    
    # Create a custom configuration
    config = Config()
    config.update(
        cleaners={
            "text": {
                "convert_case": "lower",
                "trim_whitespace": True
            },
            "number": {
                "remove_formatting": True,
                "convert_to_type": "float"
            },
            "datetime": {
                "output_format": "%Y-%m-%d"
            }
        }
    )
    
    # Example 1: Text Cleaning
    print("1. Text Cleaning")
    text_cleaner = TextCleaner(config=config)
    
    text_examples = [
        "   Hello, WORLD!   ",
        "This has numbers 123 and special chars!@#",
        "\tMultiple\nlines\twith\twhitespace\t"
    ]
    
    for text in text_examples:
        cleaned = text_cleaner.clean(text)
        print(f"   Original: '{text}'")
        print(f"   Cleaned:  '{cleaned}'")
    
    print()
    
    # Example 2: Number Cleaning
    print("2. Number Cleaning")
    number_cleaner = NumberCleaner(config=config)
    
    number_examples = [
        "$1,234.56",
        "123,456.78 USD",
        "98.6°F"
    ]
    
    for number in number_examples:
        cleaned = number_cleaner.clean(number)
        print(f"   Original: '{number}'")
        print(f"   Cleaned:  {cleaned} (type: {type(cleaned).__name__})")
    
    print()
    
    # Example 3: DateTime Cleaning
    print("3. DateTime Cleaning")
    datetime_cleaner = DateTimeCleaner(config=config)
    
    datetime_examples = [
        "2023-01-15",
        "15/01/2023 14:30",
        "Jan 15, 2023 2:30 PM"
    ]
    
    for dt_str in datetime_examples:
        cleaned = datetime_cleaner.clean(dt_str)
        print(f"   Original: '{dt_str}'")
        print(f"   Cleaned:  {cleaned}")
    
    print()
    
    # Example 4: Email Cleaning
    print("4. Email Cleaning")
    email_cleaner = EmailCleaner()
    
    email_examples = [
        "user@example.com",
        "USER.NAME+tag@EXAMPLE.CO.UK",
        "invalid-email"
    ]
    
    for email in email_examples:
        try:
            cleaned = email_cleaner.clean(email)
            print(f"   Original: '{email}'")
            print(f"   Cleaned:  {cleaned}")
        except Exception as e:
            print(f"   Original: '{email}'")
            print(f"   Error:    {str(e)}")
    
    print()
    
    # Example 5: URL Cleaning
    print("5. URL Cleaning")
    url_cleaner = URLCleaner()
    
    url_examples = [
        "www.example.com",
        "http://example.com/path",
        "https://www.example.com:8080/path?query=123#fragment"
    ]
    
    for url in url_examples:
        cleaned = url_cleaner.clean(url)
        print(f"   Original: '{url}'")
        print(f"   Cleaned:  {cleaned}")
    
    print()
    
    # Generate a cleaning report
    print("=== Generating Cleaning Report ===")
    cleaning_data = {
        "original_data": text_examples,
        "cleaned_data": [text_cleaner.clean(text) for text in text_examples],
        "cleaning_results": {
            "total_records": len(text_examples),
            "cleaned_records": len(text_examples),
            "failed_records": 0,
            "cleaned_fields": {"text": len(text_examples)},
            "cleaning_operations": [
                {"name": "trim_whitespace", "count": len(text_examples)},
                {"name": "convert_case", "count": len(text_examples)}
            ]
        }
    }
    
    report = generate_report(cleaning_data, report_type="cleaning")
    print(f"Report Type: {report['report_type']}")
    print(f"Generated At: {report['generated_at']}")
    print(f"Success Rate: {report['summary']['cleaning_success_rate']:.2f}%")


if __name__ == "__main__":
    main()

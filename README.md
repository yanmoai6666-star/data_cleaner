# Data Cleaner

A comprehensive data cleaning and transformation library for Python, designed to simplify the process of preparing data for analysis and machine learning.

## Features

### Data Cleaning
- **Text Cleaning**: Remove special characters, convert case, trim whitespace, and more
- **Number Cleaning**: Format currency, percentages, and numeric values
- **DateTime Cleaning**: Parse and format various date/time formats
- **Email Cleaning**: Validate and normalize email addresses
- **URL Cleaning**: Normalize and validate URLs

### Data Transformation
- **Text Transformation**: Tokenization, stop word removal, stemming, and n-gram generation
- **Number Transformation**: Normalization, standardization, and discretization
- **DateTime Transformation**: Extract components, calculate durations, and convert time zones
- **Categorical Transformation**: Label encoding, frequency encoding, and one-hot encoding

### Utilities
- **Data I/O**: Load and save data in CSV, JSON, Excel, and Parquet formats
- **Validation**: Validate data types, ranges, and formats
- **Reporting**: Generate detailed cleaning and transformation reports
- **Logging**: Comprehensive logging system

## Installation

### Basic Installation
```bash
pip install data_cleaner
```

### Installation with Development Dependencies
```bash
pip install -e .[dev]
```

## Quick Start

### Text Cleaning
```python
from data_cleaner import TextCleaner

# Create a text cleaner instance
cleaner = TextCleaner()

# Clean a single text string
cleaned_text = cleaner.clean("   Hello, WORLD!   ")
print(cleaned_text)  # Output: "hello, world!"

# Clean a list of text strings
texts = ["   Text 1   ", "TEXT 2", "text 3!"]
cleaned_texts = cleaner.clean_batch(texts)
print(cleaned_texts)  # Output: ["text 1", "text 2", "text 3"]
```

### Number Cleaning
```python
from data_cleaner import NumberCleaner

# Create a number cleaner instance
cleaner = NumberCleaner()

# Clean a currency string
cleaned_number = cleaner.clean("$1,234.56")
print(cleaned_number)  # Output: 1234.56

# Clean a percentage string
cleaned_percentage = cleaner.clean("98.6%")
print(cleaned_percentage)  # Output: 0.986
```

### DateTime Cleaning
```python
from data_cleaner import DateTimeCleaner

# Create a datetime cleaner instance
cleaner = DateTimeCleaner()

# Clean a date string
cleaned_date = cleaner.clean("15/01/2023 14:30")
print(cleaned_date)  # Output: 2023-01-15 14:30:00

# Format the output
cleaner.config.update("cleaners.datetime.output_format", "%Y-%m-%d")
formatted_date = cleaner.clean("15/01/2023 14:30")
print(formatted_date)  # Output: 2023-01-15
```

### Data Transformation
```python
from data_cleaner import TextTransformer

# Create a text transformer instance
transformer = TextTransformer()

# Tokenize text
tokens = transformer.tokenize("Hello world, how are you?")
print(tokens)  # Output: ["hello", "world", "how", "are", "you"]

# Generate n-grams
ngrams = transformer.generate_ngrams("Hello world", n=2)
print(ngrams)  # Output: ["hello world"]
```

### Configuration

You can customize the behavior of cleaners and transformers using the `Config` class:

```python
from data_cleaner import Config, TextCleaner

# Create a custom configuration
config = Config()
config.update({
    "cleaners": {
        "text": {
            "convert_case": "upper",
            "trim_whitespace": True,
            "remove_special_chars": True
        }
    }
})

# Use the custom configuration
cleaner = TextCleaner(config=config)
cleaned_text = cleaner.clean("   hello, world!   ")
print(cleaned_text)  # Output: "HELLO WORLD"
```

## Documentation

For detailed documentation, please refer to the [documentation](https://data_cleaner.readthedocs.io/).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Create a pull request

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Your Name - [@yourusername](https://github.com/yourusername)

## Acknowledgments

- This library was inspired by the need for a simple yet powerful data cleaning tool
- Special thanks to all contributors

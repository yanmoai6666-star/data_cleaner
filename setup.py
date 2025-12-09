#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for the data_cleaner package.
"""

from setuptools import setup, find_packages
from pathlib import Path
import os


def get_version():
    """
    Get the version from the __init__.py file.
    """
    init_file = Path(__file__).parent / "data_cleaner" / "__init__.py"
    with open(init_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split("=")[1].strip().strip('"')
    raise ValueError("Version not found in __init__.py")


def get_long_description():
    """
    Get the long description from the README.md file.
    """
    readme_file = Path(__file__).parent / "README.md"
    if readme_file.exists():
        with open(readme_file, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# Setup configuration
setup(
    name="data_cleaner",
    version=get_version(),
    description="A comprehensive data cleaning and transformation library for Python",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/data_cleaner",
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    package_data={
        "data_cleaner": [
            "config/*.json",
            "utils/*.py"
        ]
    },
    include_package_data=True,
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "python-dateutil>=2.8.0",
        "regex>=2021.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "flake8>=3.9.0",
            "black>=21.0.0",
            "isort>=5.0.0",
            "mypy>=0.800",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0"
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "tox>=3.20.0"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    keywords="data cleaning data preparation data transformation",
    project_urls={
        "Documentation": "https://data_cleaner.readthedocs.io/",
        "Bug Reports": "https://github.com/yourusername/data_cleaner/issues",
        "Source": "https://github.com/yourusername/data_cleaner/",
    },
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "data_cleaner=data_cleaner.cli:main",
        ],
    },
)

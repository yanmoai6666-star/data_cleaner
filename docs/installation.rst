Installation
============

This section describes how to install the data_cleaner package.

Prerequisites
-------------

- Python 3.7 or higher
- pip (Python package installer)

Basic Installation
------------------

You can install the data_cleaner package directly from PyPI using pip:

.. code-block:: bash

    pip install data_cleaner

Installation from Source
------------------------

If you want to install the package from source, follow these steps:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/yourusername/data_cleaner.git

2. Change to the repository directory:

   .. code-block:: bash

       cd data_cleaner

3. Install the package in development mode:

   .. code-block:: bash

       pip install -e .

Installation with Development Dependencies
------------------------------------------

To install the package with development dependencies (for testing, documentation, etc.):

.. code-block:: bash

    pip install -e .[dev]

This will install the following development dependencies:

- pytest (for testing)
- pytest-cov (for test coverage)
- flake8 (for code style checking)
- black (for code formatting)
- isort (for import sorting)
- mypy (for static type checking)
- sphinx (for documentation)
- sphinx-rtd-theme (for documentation theme)
- tox (for testing across multiple Python versions)

Verifying the Installation
--------------------------

To verify that the installation was successful, you can import the package and check its version:

.. code-block:: python

    import data_cleaner
    print(data_cleaner.__version__)

This should print the version number of the installed package.

# NiFi Python Scripts

## Installing Poetry

### On Mac

Open your terminal and run:

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

or

  ```bash
  brew install poetry
  ```

### On Windows

1. **Install Poetry**:
    Open PowerShell and run:

    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    ```

2. **Add Poetry to your PATH**:
    Add the Poetry installation path to your system environment variables. Typically, this is  `C:\Users\<YourUsername>\AppData\Roaming\Python\Scripts`.

### Installing Dependencies

1. **Navigate to your project directory**:

    ```bash
    cd /path/to/this/project
    ```

2. **Install dependencies**:

    ```bash
    poetry install
    ```

### Running Tests

  ```bash
  poetry run pytest
  ```

### Running Tests with Coverage Report

  ```bash
  poetry run pytest -s --cov=src --cov-report=xml
  ```

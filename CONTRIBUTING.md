# Contributing to Borsdata API Client

Thank you for considering contributing to the Borsdata API Client! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name` or `git checkout -b fix/your-bugfix-name`
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality: `pytest`
5. Commit your changes with a descriptive commit message
6. Push your branch to your fork: `git push origin your-branch-name`
7. Create a pull request to the main repository

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install development dependencies: `pip install -r requirements-dev.txt`
5. Create a `.env` file with your Borsdata API key:
   ```
   BORSDATA_API_KEY=your_api_key_here
   ```

## Testing

Run tests with pytest:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=src/borsdata_client tests/
```

## Code Style

This project follows PEP 8 style guidelines with a line length of 88 characters. We use Black for code formatting and isort for import sorting.

Format your code before submitting:

```bash
black src tests
isort src tests
```

## Type Hints

All code should include proper type hints according to PEP 484.

## Documentation

Please update documentation when adding or modifying features. This includes:

- Docstrings for new functions, methods, and classes
- Updates to README.md if necessary
- New or updated examples in the docs directory

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation if necessary
3. The PR should work for Python 3.7 and above
4. Your PR will be reviewed by maintainers, who may request changes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

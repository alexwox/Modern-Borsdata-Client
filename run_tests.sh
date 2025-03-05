#!/bin/bash

# Run unit tests by default
if [ "$1" == "--all" ]; then
    echo "Running all tests..."
    python -m pytest
elif [ "$1" == "--integration" ]; then
    echo "Running integration tests..."
    python -m pytest -m "integration"
elif [ "$1" == "--coverage" ]; then
    echo "Running tests with coverage report..."
    python -m pytest --cov=src --cov-report=term-missing
elif [ "$1" == "--models" ]; then
    echo "Running model tests only..."
    python -m pytest tests/test_models.py tests/test_model_validation.py
elif [ "$1" == "--edge-cases" ]; then
    echo "Running edge case tests only..."
    python -m pytest tests/test_edge_cases.py
elif [ "$1" == "--performance" ]; then
    echo "Running performance tests..."
    python -m pytest -m "performance"
else
    echo "Running unit tests only..."
    python -m pytest -m "not integration and not performance"
fi 
#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Run tests
if [ "$1" == "--all" ]; then
    echo "Running all tests..."
    python -m pytest
elif [ "$1" == "--integration" ]; then
    echo "Running integration tests..."
    python -m pytest tests/test_integration.py -v
elif [ "$1" == "--coverage" ]; then
    echo "Running tests with coverage report..."
    python3 -m pytest --cov=src --cov-report=term-missing
elif [ "$1" == "--models" ]; then
    echo "Running model tests only..."
    python3 -m pytest tests/test_models.py tests/test_model_validation.py
elif [ "$1" == "--endpoints" ]; then
    echo "Running client tests only..."
    python3 -m pytest tests/test_endpoints.py 
elif [ "$1" == "--edge-cases" ]; then
    echo "Running edge case tests only..."
    python3 -m pytest tests/test_edge_cases.py
elif [ "$1" == "--performance" ]; then
    echo "Running performance tests..."
    python -m pytest tests/test_performance.py -v
else
    echo "Running unit tests..."
    python -m pytest tests/test_client.py tests/test_models.py tests/test_errors.py tests/test_edge_cases.py tests/test_model_validation.py
fi 
# BorsdataClient Tests

This directory contains tests for the BorsdataClient library.

## Test Structure

- `conftest.py`: Contains pytest fixtures and configuration
- `test_client.py`: Tests for the BorsdataClient class
- `test_endpoints.py`: Tests for the BorsdataClient API endpoints
- `test_integration.py`: Integration tests that make real API calls
- `test_models.py`: Tests for the Pydantic models
- `test_model_validation.py`: Tests for model validation
- `test_edge_cases.py`: Tests for edge cases and error handling
- `test_performance.py`: Performance tests for the client
- `test_errors.py`: Tests for the BorsdataClientError class

## Running Tests

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
./run_tests.sh --all
```

### Run Unit Tests Only

```bash
./run_tests.sh
```

### Run Integration Tests Only

```bash
./run_tests.sh --integration
```

### Run Model Tests Only

```bash
./run_tests.sh --models
```

### Run Endpoint Tests Only

```bash
./run_tests.sh --endpoints
```

### Run Edge Case Tests Only

```bash
./run_tests.sh --edge-cases
```

### Run Performance Tests

```bash
./run_tests.sh --performance
```

### Run Tests with Coverage Report

```bash
./run_tests.sh --coverage
```

## Integration Tests

Integration tests make real API calls to the Borsdata API. To run these tests, you need to set the `BORSDATA_API_KEY` environment variable:

```bash
export BORSDATA_API_KEY=your_api_key
./run_tests.sh --integration
```

These tests are skipped by default if no API key is available.

## Performance Tests

Performance tests measure the execution time of various client methods. They are skipped by default to avoid unnecessary API calls. To run these tests, you need to set the `BORSDATA_API_KEY` environment variable:

```bash
export BORSDATA_API_KEY=your_api_key
./run_tests.sh --performance
```

## Mock Responses

The unit tests use mock responses to avoid making real API calls. The mock responses are stored in the `fixtures` directory and are created automatically when running the tests.

## Adding New Tests

When adding new tests:

1. For unit tests, add a new test function to the appropriate test file
2. For integration tests, add a new test function to `test_integration.py`
3. For model tests, add a new test function to `test_models.py` or `test_model_validation.py`
4. For edge case tests, add a new test function to `test_edge_cases.py`
5. For performance tests, add a new test function to `test_performance.py`
6. Make sure to add appropriate assertions to verify the behavior

"""Pytest configuration and fixtures for testing the BorsdataClient."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Callable

import pytest
from httpx import Response

from src.borsdata_client.client import BorsdataClient


class MockResponse(Response):
    """Mock Response for testing."""
    
    def __init__(self, status_code: int, json_data: Dict[str, Any]):
        self.status_code = status_code
        self._json_data = json_data
        super().__init__(status_code)
    
    def json(self) -> Dict[str, Any]:
        """Return the JSON data."""
        return self._json_data


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock BorsdataClient that doesn't make real API calls."""
    client = BorsdataClient("test_api_key")
    
    def mock_get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mock the _get method to return test data."""
        # Convert endpoint to a filename-friendly format
        endpoint_parts = endpoint.strip('/').split('/')
        filename = '_'.join(endpoint_parts) + '.json'
        
        # Look for the mock response file in the fixtures directory
        fixtures_dir = Path(__file__).parent / 'fixtures'
        fixture_path = fixtures_dir / filename
        
        if fixture_path.exists():
            with open(fixture_path, 'r') as f:
                return json.load(f)
        else:
            # If no fixture file exists, return an empty response
            return {}
    
    # Replace the _get method with our mock
    monkeypatch.setattr(client, '_get', mock_get.__get__(client))
    
    return client


@pytest.fixture
def api_key():
    """Return the API key from environment or a test key."""
    return os.environ.get('BORSDATA_API_KEY', 'test_api_key')


@pytest.fixture
def real_client(api_key):
    """Create a real BorsdataClient for integration tests."""
    return BorsdataClient(api_key) 
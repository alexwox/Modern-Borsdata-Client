"""Pytest configuration and fixtures for testing the BorsdataClient."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict

import pytest
from httpx import Response

from borsdata_client.client import BorsdataClient


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
        print(f"[Mock Client]: endpoint: {endpoint}")
        endpoint_parts = endpoint.strip("/").split("/")
        filename = "_".join(endpoint_parts) + ".json"

        # Look for the mock response file in the fixtures directory
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixture_path = fixtures_dir / filename
        print(f"[Mock Client]: Looking for fixture file: {fixture_path}")
        if fixture_path.exists():
            print(f"[Mock Client]: Using fixture file: {fixture_path}")
            with open(fixture_path, "r") as f:
                return json.load(f)
        else:
            # If no fixture file exists, return an appropriate empty response
            # based on the endpoint
            if endpoint == "/instruments/kpis/metadata":
                return {"kpiHistoryMetadatas": []}
            elif endpoint.startswith("/holdings/insider"):
                return {"list": []}
            elif endpoint.startswith("/holdings/shorts"):
                return {"list": []}
            elif endpoint.startswith("/holdings/buyback"):
                return {"list": []}
            elif endpoint.startswith("/instruments/description"):
                return {"list": []}
            elif endpoint.startswith("/instruments/report/calendar"):
                return {"list": []}
            elif endpoint.startswith("/instruments/dividend/calendar"):
                return {"list": []}
            elif endpoint.startswith(
                "/instruments/stockprices/date"
            ) or endpoint.startswith("/instruments/stockprices/global/date"):
                return {"stockPricesList": []}
            elif endpoint.startswith(
                "/instruments/stockprices/last"
            ) or endpoint.startswith("/instruments/stockprices/global/last"):
                return {"stockPricesList": []}
            elif endpoint == "/translationmetadata":
                return {"translationMetadatas": []}

            else:
                return {}

    # Replace the _get method with our mock
    monkeypatch.setattr(client, "_get", mock_get.__get__(client))

    return client


@pytest.fixture
def api_key():
    """Return the API key from environment or a test key."""
    return os.environ.get("BORSDATA_API_KEY", "test_api_key")


@pytest.fixture
def real_client(api_key):
    """Create a real BorsdataClient for integration tests."""
    return BorsdataClient(api_key)

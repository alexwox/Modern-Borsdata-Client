"""Tests for the BorsdataClient class."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.borsdata_client.client import BorsdataClient, BorsdataClientError


def test_client_initialization():
    """Test that the client can be initialized with an API key."""
    client = BorsdataClient("test_api_key")
    assert client.api_key == "test_api_key"
    assert client.BASE_URL == "https://apiservice.borsdata.se/v1"


def test_client_context_manager():
    """Test that the client can be used as a context manager."""
    with BorsdataClient("test_api_key") as client:
        assert client.api_key == "test_api_key"


@patch("httpx.Client.get")
def test_get_method_success(mock_get):
    """Test the _get method with a successful response."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_get.return_value = mock_response

    # Create client and call _get
    client = BorsdataClient("test_api_key")
    result = client._get("/test/endpoint")

    # Verify the result
    assert result == {"test": "data"}
    mock_get.assert_called_once_with(
        f"{client.BASE_URL}/test/endpoint", params={"authKey": "test_api_key"}
    )


@patch("httpx.Client.get")
def test_get_method_with_params(mock_get):
    """Test the _get method with additional parameters."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_get.return_value = mock_response

    # Create client and call _get with params
    client = BorsdataClient("test_api_key")
    result = client._get("/test/endpoint", params={"param1": "value1"})

    # Verify the result
    assert result == {"test": "data"}
    mock_get.assert_called_once_with(
        f"{client.BASE_URL}/test/endpoint",
        params={"authKey": "test_api_key", "param1": "value1"},
    )


@patch("httpx.Client.get")
def test_get_method_error(mock_get):
    """Test the _get method with an error response."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}
    # Add raise_for_status method that raises an exception
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Bad Request", request=MagicMock(), response=mock_response
    )
    mock_get.return_value = mock_response

    # Create client and call _get
    client = BorsdataClient("test_api_key")

    # Verify that an exception is raised
    with pytest.raises(BorsdataClientError) as excinfo:
        client._get("/test/endpoint")

    assert "API request failed with status code 400" in str(excinfo.value)


@patch("httpx.Client.get")
def test_get_method_connection_error(mock_get):
    """Test the _get method with a connection error."""
    # Setup mock to raise an exception
    mock_get.side_effect = Exception("Connection error")

    # Create client and call _get
    client = BorsdataClient("test_api_key")

    # Verify that an exception is raised
    with pytest.raises(BorsdataClientError) as excinfo:
        client._get("/test/endpoint")

    assert "API request failed: Connection error" in str(excinfo.value)

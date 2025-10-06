"""Tests for the BorsdataClientError class."""

import pytest

from borsdata_client.client import BorsdataClientError


def test_borsdata_client_error():
    """Test that the BorsdataClientError can be raised with a message."""
    error_message = "Test error message"

    # Verify that the error can be raised with a message
    with pytest.raises(BorsdataClientError) as excinfo:
        raise BorsdataClientError(error_message)

    # Verify that the error message is correct
    assert str(excinfo.value) == error_message


def test_borsdata_client_error_with_status_code():
    """Test that the BorsdataClientError can be raised with a status code."""
    status_code = 400
    error_message = f"API request failed with status code {status_code}"

    # Verify that the error can be raised with a status code
    with pytest.raises(BorsdataClientError) as excinfo:
        raise BorsdataClientError(error_message)

    # Verify that the error message is correct
    assert str(excinfo.value) == error_message
    assert "status code 400" in str(excinfo.value)

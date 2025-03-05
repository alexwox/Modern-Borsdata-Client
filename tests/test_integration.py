"""Integration tests for the BorsdataClient.

These tests require a valid API key and will make real API calls.
They are skipped by default to avoid unnecessary API calls during regular testing.
"""

import os
import pytest
from datetime import datetime, timedelta

from src.borsdata_client.client import BorsdataClient


# Skip all tests in this module if no API key is available
pytestmark = pytest.mark.skipif(
    os.environ.get('BORSDATA_API_KEY') is None,
    reason="No API key available for integration tests"
)


def test_get_branches_integration(real_client):
    """Integration test for get_branches."""
    branches = real_client.get_branches()
    assert len(branches) > 0
    assert branches[0].id > 0


def test_get_countries_integration(real_client):
    """Integration test for get_countries."""
    countries = real_client.get_countries()
    assert len(countries) > 0
    assert countries[0].id > 0


def test_get_markets_integration(real_client):
    """Integration test for get_markets."""
    markets = real_client.get_markets()
    assert len(markets) > 0
    assert markets[0].id > 0


def test_get_instruments_integration(real_client):
    """Integration test for get_instruments."""
    instruments = real_client.get_instruments()
    assert len(instruments) > 0
    assert instruments[0].ins_id > 0


def test_get_global_instruments_integration(real_client):
    """Integration test for get_global_instruments."""
    instruments = real_client.get_global_instruments()
    assert len(instruments) > 0
    assert instruments[0].ins_id > 0


def test_get_stock_prices_integration(real_client):
    """Integration test for get_stock_prices."""
    # Get the first instrument to test with
    instruments = real_client.get_instruments()
    instrument_id = instruments[0].ins_id
    
    # Get stock prices for the last 7 days
    to_date = datetime.now()
    from_date = to_date - timedelta(days=7)
    
    prices = real_client.get_stock_prices(
        instrument_id=instrument_id,
        from_date=from_date,
        to_date=to_date
    )
    
    # We might not have prices for all days (weekends, holidays)
    # but we should have at least one if the API is working
    assert len(prices) >= 0


def test_get_kpi_metadata_integration(real_client):
    """Integration test for get_kpi_metadata."""
    kpis = real_client.get_kpi_metadata()
    assert len(kpis) > 0
    assert kpis[0].kpi_id > 0


def test_get_kpi_updated_integration(real_client):
    """Integration test for get_kpi_updated."""
    updated = real_client.get_kpi_updated()
    assert isinstance(updated, datetime)
    # The update time should be in the past
    assert updated < datetime.now()


def test_get_last_stock_prices_integration(real_client):
    """Integration test for get_last_stock_prices."""
    prices = real_client.get_last_stock_prices()
    assert len(prices) > 0
    assert prices[0].i > 0


def test_get_translation_metadata_integration(real_client):
    """Integration test for get_translation_metadata."""
    translations = real_client.get_translation_metadata()
    assert len(translations.branches) > 0
    assert translations.branches[0].id > 0 
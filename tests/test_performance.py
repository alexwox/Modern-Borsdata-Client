"""Performance tests for the BorsdataClient.

These tests measure the performance of the client methods.
They are marked as 'performance' and are skipped by default.
"""

import time
import pytest
from datetime import datetime, timedelta

from src.borsdata_client.client import BorsdataClient


# Mark all tests in this module as performance tests
pytestmark = [
    pytest.mark.performance,
    pytest.mark.skipif(True, reason="Performance tests are skipped by default")
]


@pytest.fixture
def performance_client(api_key):
    """Create a client for performance testing."""
    return BorsdataClient(api_key)


def test_get_instruments_performance(performance_client):
    """Test the performance of get_instruments."""
    start_time = time.time()
    instruments = performance_client.get_instruments()
    end_time = time.time()
    
    assert len(instruments) > 0
    
    # Log the performance
    duration = end_time - start_time
    print(f"\nget_instruments took {duration:.2f} seconds for {len(instruments)} instruments")
    print(f"Average time per instrument: {(duration / len(instruments)) * 1000:.2f} ms")


def test_get_stock_prices_performance(performance_client):
    """Test the performance of get_stock_prices."""
    # Get the first instrument to test with
    instruments = performance_client.get_instruments()
    instrument_id = instruments[0].ins_id
    
    # Get stock prices for the last 30 days
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    
    start_time = time.time()
    prices = performance_client.get_stock_prices(
        instrument_id=instrument_id,
        from_date=from_date,
        to_date=to_date
    )
    end_time = time.time()
    
    # Log the performance
    duration = end_time - start_time
    print(f"\nget_stock_prices took {duration:.2f} seconds for {len(prices)} prices")
    if prices:
        print(f"Average time per price: {(duration / len(prices)) * 1000:.2f} ms")


def test_get_reports_performance(performance_client):
    """Test the performance of get_reports."""
    # Get the first instrument to test with
    instruments = performance_client.get_instruments()
    instrument_id = instruments[0].ins_id
    
    start_time = time.time()
    reports = performance_client.get_reports(
        instrument_id=instrument_id,
        report_type="year",
        max_count=10
    )
    end_time = time.time()
    
    # Log the performance
    duration = end_time - start_time
    print(f"\nget_reports took {duration:.2f} seconds for {len(reports)} reports")
    if reports:
        print(f"Average time per report: {(duration / len(reports)) * 1000:.2f} ms")


def test_get_kpi_metadata_performance(performance_client):
    """Test the performance of get_kpi_metadata."""
    start_time = time.time()
    kpis = performance_client.get_kpi_metadata()
    end_time = time.time()
    
    assert len(kpis) > 0
    
    # Log the performance
    duration = end_time - start_time
    print(f"\nget_kpi_metadata took {duration:.2f} seconds for {len(kpis)} KPIs")
    print(f"Average time per KPI: {(duration / len(kpis)) * 1000:.2f} ms")


def test_get_last_stock_prices_performance(performance_client):
    """Test the performance of get_last_stock_prices."""
    start_time = time.time()
    prices = performance_client.get_last_stock_prices()
    end_time = time.time()
    
    assert len(prices) > 0
    
    # Log the performance
    duration = end_time - start_time
    print(f"\nget_last_stock_prices took {duration:.2f} seconds for {len(prices)} prices")
    print(f"Average time per price: {(duration / len(prices)) * 1000:.2f} ms")


def test_batch_requests_performance(performance_client):
    """Test the performance of making multiple requests in sequence."""
    start_time = time.time()
    
    # Make a series of requests
    branches = performance_client.get_branches()
    countries = performance_client.get_countries()
    markets = performance_client.get_markets()
    instruments = performance_client.get_instruments()
    kpis = performance_client.get_kpi_metadata()
    
    end_time = time.time()
    
    # Log the performance
    duration = end_time - start_time
    total_items = len(branches) + len(countries) + len(markets) + len(instruments) + len(kpis)
    print(f"\nBatch requests took {duration:.2f} seconds for {total_items} total items")
    print(f"Average time per item: {(duration / total_items) * 1000:.2f} ms")


def test_concurrent_requests_performance(performance_client):
    """Test the performance of making concurrent requests.
    
    Note: This test requires the 'concurrent.futures' module.
    """
    try:
        import concurrent.futures
    except ImportError:
        pytest.skip("concurrent.futures module not available")
    
    # Define the requests to make
    requests = [
        lambda: performance_client.get_branches(),
        lambda: performance_client.get_countries(),
        lambda: performance_client.get_markets(),
        lambda: performance_client.get_instruments(),
        lambda: performance_client.get_kpi_metadata()
    ]
    
    start_time = time.time()
    
    # Make concurrent requests
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(request) for request in requests]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    end_time = time.time()
    
    # Log the performance
    duration = end_time - start_time
    total_items = sum(len(result) for result in results)
    print(f"\nConcurrent requests took {duration:.2f} seconds for {total_items} total items")
    print(f"Average time per item: {(duration / total_items) * 1000:.2f} ms") 
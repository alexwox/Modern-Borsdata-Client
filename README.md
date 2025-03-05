# Borsdata API Client

A modern Python client for the Borsdata API, featuring:

- Full type hints and modern Python features
- Pydantic models for request/response validation
- Async HTTP client with connection pooling
- Comprehensive error handling
- Context manager support
- Intuitive API design

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from borsdata_client import BorsdataClient
from datetime import datetime, timedelta

# Initialize the client
api_key = "your_api_key_here"
client = BorsdataClient(api_key)

# Use as a context manager (recommended)
with BorsdataClient(api_key) as client:
    # Get all instruments
    instruments = client.get_instruments()

    # Get stock prices for an instrument
    today = datetime.now()
    last_month = today - timedelta(days=30)
    prices = client.get_stock_prices(
        instrument_id=3,  # Example ID
        from_date=last_month,
        to_date=today
    )

    # Get financial reports
    reports = client.get_reports(
        instrument_id=3,
        report_type="year",
        max_count=5
    )

# The client will automatically close the connection when exiting the context
```

## Documentation

Comprehensive documentation is available in the `docs` directory:

- [Getting Started Guide](docs/guides/getting_started.md) - Learn how to install and use the library
- [Advanced Usage Guide](docs/guides/advanced_usage.md) - Explore advanced features and usage patterns
- [API Reference](docs/api/client.md) - Comprehensive reference for the BorsdataClient class
- [Models Reference](docs/api/models.md) - Reference for the Pydantic models used in the library
- [Examples](docs/examples/basic_usage.md) - Code examples to get you started

## Available Methods

- `get_branches()` - Get all branches/industries
- `get_countries()` - Get all countries
- `get_markets()` - Get all markets
- `get_instruments()` - Get all Nordic instruments
- `get_global_instruments()` - Get all global instruments (Pro+ subscription required)
- `get_stock_prices()` - Get stock prices for an instrument
- `get_reports()` - Get financial reports for an instrument
- `get_kpi_metadata()` - Get metadata for all KPIs
- `get_insider_holdings()` - Get insider holdings for instruments
- `get_short_positions()` - Get short positions for all instruments
- `get_buybacks()` - Get buybacks for instruments
- `get_instrument_descriptions()` - Get descriptions for instruments
- `get_report_calendar()` - Get report calendar for instruments
- `get_dividend_calendar()` - Get dividend calendar for instruments
- `get_kpi_history()` - Get KPI history for an instrument
- `get_kpi_updated()` - Get last update time for KPIs
- `get_last_stock_prices()` - Get last stock prices for all instruments
- `get_last_global_stock_prices()` - Get last stock prices for all global instruments
- `get_stock_prices_by_date()` - Get stock prices for all instruments on a specific date
- `get_global_stock_prices_by_date()` - Get stock prices for all global instruments on a specific date
- `get_stock_splits()` - Get stock splits
- `get_translation_metadata()` - Get translation metadata

## Error Handling

The client includes comprehensive error handling:

```python
from borsdata_client import BorsdataClient, BorsdataClientError

try:
    with BorsdataClient(api_key) as client:
        instruments = client.get_instruments()
except BorsdataClientError as e:
    print(f"API request failed: {e}")
```

## Data Models

All API responses are validated and converted to Pydantic models. See the [Models Reference](docs/api/models.md) for details.

## Requirements

- Python 3.7+
- pydantic>=2.5.2
- httpx>=0.25.2
- python-dateutil>=2.8.2
- typing-extensions>=4.8.0

## License

MIT License

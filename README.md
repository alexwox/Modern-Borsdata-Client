# Borsdata API Client

### [NOT AFFILIATED WITH BÖRSDATA]

### [THIS IS A THIRD PARTY LIBRARY]

This is a modern Python client for the Borsdata API, featuring:

- Full type hints and modern Python features
- Pydantic models for request/response validation
- Async HTTP client with connection pooling
- Comprehensive error handling
- Context manager support
- Intuitive API design

For the official documentation check out:
[https://github.com/Borsdata-Sweden/API]

## Installation

### From Source

```bash
git clone https://github.com/yourusername/modern-borsdata-client.git
cd modern-borsdata-client
pip install -e .
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

    # Get stock prices for a specific instrument
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    stock_prices = client.get_stock_prices(
        instrument_id=instruments[0].insId,
        from_date=one_year_ago,
        to_date=today
    )

    # Print the results
    print(f"Found {len(instruments)} instruments")
    print(f"Got {len(stock_prices)} price points for {instruments[0].name}")
```

## Using in Your Projects

### As a Dependency

Add to your project's requirements.txt:

```
borsdata-client>=0.1.0
```

Or in your pyproject.toml:

```toml
[project]
dependencies = [
    "borsdata-client>=0.1.0",
]
```

### Environment Variables

For better security, you can store your API key in an environment variable:

```python
import os
from borsdata_client import BorsdataClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("BORSDATA_API_KEY")

# Initialize client
client = BorsdataClient(api_key)
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
- `get_sectors()` - Get all sectors
- `get_instruments()` - Get all Nordic instruments
- `get_global_instruments()` - Get all global instruments (Pro+ subscription required)
- `get_stock_prices()` - Get stock prices for an instrument
- `get_stock_prices_batch()` - Get stock prices for a batch of instrument
- `get_reports()` - Get financial reports for an instrument
- `get_reports_metadata()` - Get metadata for all financial report values
- `get_kpi_metadata()` - Get metadata for all KPIs
- `get_kpi_updated()` - Get last update time for KPIs
- `get_kpi_history()` - Get one KPIs history for an instrument
- `get_kpi_summary()` - Get summary of KPIs history for an instrument (Note: Not all kpi's)
- `get_insider_holdings()` - Get insider holdings for instruments
- `get_short_positions()` - Get short positions for all instruments
- `get_buybacks()` - Get buybacks for instruments
- `get_instrument_descriptions()` - Get descriptions for instruments
- `get_report_calendar()` - Get report calendar for instruments
- `get_dividend_calendar()` - Get dividend calendar for instruments
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

Retries five times by default if reaching the APIs rate limit (100 requests / 10 seconds).

## Data Models

All API responses are validated and converted to Pydantic models. See the [Models Reference](docs/api/models.md) for details.

## Requirements

- Python 3.7+
- pydantic>=2.5.2
- httpx>=0.25.2
- python-dateutil>=2.8.2
- typing-extensions>=4.8.0
- tenacity>=9.0.0

## License

MIT License

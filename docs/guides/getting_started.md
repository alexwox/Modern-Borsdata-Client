# Getting Started with BorsdataClient

This guide will help you get started with the BorsdataClient library for accessing financial data from the Borsdata API.

## Prerequisites

Before you begin, you'll need:

- Python 3.7 or higher
- A Borsdata API key (obtain one from [Borsdata](https://borsdata.se/))
- Basic knowledge of Python

## Installation

Install the BorsdataClient library using pip:

```bash
pip install -r requirements.txt
```

## Basic Usage

Here's a simple example to get you started:

```python
from borsdata_client import BorsdataClient
from datetime import datetime, timedelta

# Initialize the client with your API key
api_key = "your_api_key_here"
client = BorsdataClient(api_key)

# Get all available instruments (stocks)
instruments = client.get_instruments()

# Print the first 5 instruments
for instrument in instruments[:5]:
    print(f"ID: {instrument.ins_id}, Name: {instrument.name}, Ticker: {instrument.ticker}")
```

## Using as a Context Manager

The recommended way to use the client is with a context manager, which ensures proper resource cleanup:

```python
with BorsdataClient("your_api_key_here") as client:
    # Your code here
    instruments = client.get_instruments()
    # The client will automatically close when exiting the context
```

## Fetching Stock Prices

To fetch stock prices for a specific instrument:

```python
with BorsdataClient("your_api_key_here") as client:
    # Get stock prices for the last 30 days
    today = datetime.now()
    last_month = today - timedelta(days=30)

    prices = client.get_stock_prices(
        instrument_id=3,  # Example: Volvo B
        from_date=last_month,
        to_date=today,
        max_count=30
    )

    for price in prices:
        print(f"Date: {price.d}, Close: {price.c}, Volume: {price.v}")
```

## Fetching Financial Reports

To fetch financial reports for a company:

```python
with BorsdataClient("your_api_key_here") as client:
    # Get the last 5 yearly reports
    reports = client.get_reports(
        instrument_id=3,
        report_type="year",  # Options: "year", "quarter", "r12"
        max_count=5
    )

    for report in reports:
        print(f"Year: {report.year}, Period: {report.period}")
        print(f"Revenues: {report.revenues}")
        print(f"Operating Income: {report.operating_income}")
        print(f"EPS: {report.earnings_per_share}")
        print("---")
```

## Error Handling

The client includes comprehensive error handling:

```python
from borsdata_client import BorsdataClient, BorsdataClientError

try:
    with BorsdataClient("your_api_key_here") as client:
        instruments = client.get_instruments()
except BorsdataClientError as e:
    print(f"API request failed: {e}")
```

## Next Steps

- Check out the [API Reference](../api/client.md) for a complete list of available methods
- Explore the [Examples](../examples/basic_usage.md) for more advanced usage patterns
- Read the [Guides](./advanced_usage.md) for in-depth explanations of specific features

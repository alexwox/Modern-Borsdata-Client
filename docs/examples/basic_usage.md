# Basic Usage Examples

This document provides basic usage examples for the BorsdataClient library.

## Setting Up the Client

```python
from borsdata_client import BorsdataClient
import os

# Get API key from environment variable (recommended)
api_key = os.environ.get("BORSDATA_API_KEY")

# Initialize the client
client = BorsdataClient(api_key)
```

## Using the Context Manager

```python
from borsdata_client import BorsdataClient
import os

# Get API key from environment variable
api_key = os.environ.get("BORSDATA_API_KEY")

# Use the client as a context manager
with BorsdataClient(api_key) as client:
    # Your code here
    pass  # The client will automatically close when exiting the context
```

## Fetching Instruments

```python
from borsdata_client import BorsdataClient
import os

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get all Nordic instruments
    instruments = client.get_instruments()

    # Print the first 5 instruments
    for instrument in instruments[:5]:
        print(f"ID: {instrument.ins_id}, Name: {instrument.name}, Ticker: {instrument.ticker}")

    # Get all global instruments (requires Pro+ subscription)
    global_instruments = client.get_global_instruments()
```

## Fetching Stock Prices

```python
from borsdata_client import BorsdataClient
from datetime import datetime, timedelta
import os

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get stock prices for the last 30 days
    today = datetime.now()
    last_month = today - timedelta(days=30)

    # Get stock prices for a specific instrument (e.g., Volvo B with ID 3)
    prices = client.get_stock_prices(
        instrument_id=3,
        from_date=last_month,
        to_date=today,
        max_count=30
    )

    # Print the stock prices
    for price in prices:
        date = price.get_date()  # Convert string date to datetime
        print(f"Date: {date.strftime('%Y-%m-%d')}, Close: {price.c}, Volume: {price.v}")
```

## Fetching Financial Reports

```python
from borsdata_client import BorsdataClient
import os

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get the last 5 yearly reports for a specific instrument
    reports = client.get_reports(
        instrument_id=3,  # Example: Volvo B
        report_type="year",  # Options: "year", "quarter", "r12"
        max_count=5
    )

    # Print the reports
    for report in reports:
        print(f"Year: {report.year}, Period: {report.period}")
        print(f"Revenues: {report.revenues}")
        print(f"Operating Income: {report.operating_income}")
        print(f"EPS: {report.earnings_per_share}")
        print("---")
```

## Fetching KPI Data

```python
from borsdata_client import BorsdataClient
import os

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get metadata for all KPIs
    kpi_metadata = client.get_kpi_metadata()

    # Print the first 5 KPIs
    for kpi in kpi_metadata[:5]:
        print(f"KPI ID: {kpi.kpi_id}, Name: {kpi.name_en}")

    # Get KPI history for a specific instrument and KPI
    kpi_history = client.get_kpi_history(
        instrument_id=3,  # Example: Volvo B
        kpi_id=1,  # Example: P/E ratio
        report_type="year",  # Options: "year", "quarter", "r12"
        price_type="mean",  # Options: "mean", "high", "low"
        max_count=10
    )

    # Print the KPI values
    for value in kpi_history.values:
        print(f"Instrument ID: {value.i}, Value: {value.n}")
```

## Error Handling

```python
from borsdata_client import BorsdataClient, BorsdataClientError
import os

api_key = os.environ.get("BORSDATA_API_KEY")

try:
    with BorsdataClient(api_key) as client:
        instruments = client.get_instruments()
except BorsdataClientError as e:
    print(f"API request failed: {e}")
```

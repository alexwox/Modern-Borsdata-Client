# Advanced Usage Guide

This guide covers advanced usage patterns and features of the BorsdataClient library.

## Working with KPIs (Key Performance Indicators)

Borsdata provides a rich set of KPIs for financial analysis. Here's how to work with them:

```python
from borsdata_client import BorsdataClient

with BorsdataClient("your_api_key_here") as client:
    # Get metadata for all available KPIs
    kpi_metadata = client.get_kpi_metadata()

    # Print available KPIs
    for kpi in kpi_metadata[:5]:  # Just showing first 5
        print(f"KPI ID: {kpi.kpi_id}, Name: {kpi.name_en}")

    # Get KPI history for a specific instrument and KPI
    kpi_history = client.get_kpi_history(
        instrument_id=3,  # Example: Volvo B
        kpi_id=1,  # Example: P/E ratio
        report_type="year",  # Options: "year", "quarter", "r12"
        price_type="mean",  # Options: "mean", "high", "low"
        max_count=10
    )

    # Process KPI values
    for value in kpi_history.values:
        print(f"Instrument ID: {value.i}, Value: {value.n}")
```

## Working with Insider Trading Data

Insider trading data can provide valuable insights:

```python
from borsdata_client import BorsdataClient

with BorsdataClient("your_api_key_here") as client:
    # Get insider trading data for specific instruments
    insider_data = client.get_insider_holdings([3, 4, 5])  # Example IDs

    # Process insider trading data
    for insider_response in insider_data:
        print(f"Instrument ID: {insider_response.list[0].ins_id}")
        for insider in insider_response.list[0].values[:5]:  # First 5 entries
            print(f"Owner: {insider.owner_name}")
            print(f"Position: {insider.owner_position}")
            print(f"Shares: {insider.shares}")
            print(f"Transaction Date: {insider.transaction_date}")
            print("---")
```

## Working with Stock Splits

Track stock splits to adjust historical price data:

```python
from borsdata_client import BorsdataClient
from datetime import datetime, timedelta

with BorsdataClient("your_api_key_here") as client:
    # Get stock splits from the last year
    one_year_ago = datetime.now() - timedelta(days=365)
    splits = client.get_stock_splits(from_date=one_year_ago)

    # Process stock splits
    for split in splits:
        print(f"Instrument ID: {split.ins_id}")
        print(f"Split Date: {split.split_date}")
        print(f"Split Ratio: {split.split_ratio}")
        print(f"Split Type: {split.split_type}")
        print("---")
```

## Working with Report and Dividend Calendars

Stay updated on upcoming financial reports and dividends:

```python
from borsdata_client import BorsdataClient

with BorsdataClient("your_api_key_here") as client:
    # Get report calendar for specific instruments
    report_calendar = client.get_report_calendar([3, 4, 5])  # Example IDs

    # Process report calendar
    for calendar in report_calendar:
        print(f"Instrument ID: {calendar.list[0].ins_id}")
        for date in calendar.list[0].values[:5]:  # First 5 entries
            print(f"Release Date: {date.release_date}")
            print(f"Report Type: {date.report_type}")
            print("---")

    # Get dividend calendar for specific instruments
    dividend_calendar = client.get_dividend_calendar([3, 4, 5])  # Example IDs

    # Process dividend calendar
    for calendar in dividend_calendar:
        print(f"Instrument ID: {calendar.list[0].ins_id}")
        for date in calendar.list[0].values[:5]:  # First 5 entries
            print(f"Excluding Date: {date.excluding_date}")
            print(f"Amount Paid: {date.amount_paid} {date.currency_short_name}")
            print("---")
```

## Efficient Data Retrieval

For large datasets, consider using more specific queries:

```python
from borsdata_client import BorsdataClient
from datetime import datetime

with BorsdataClient("your_api_key_here") as client:
    # Get stock prices for a specific date range
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)

    prices = client.get_stock_prices(
        instrument_id=3,
        from_date=start_date,
        to_date=end_date
    )

    # Get last stock prices for all instruments (more efficient than querying each)
    last_prices = client.get_last_stock_prices()

    # Get stock prices for all instruments on a specific date
    specific_date = datetime(2022, 12, 31)
    prices_by_date = client.get_stock_prices_by_date(specific_date)
```

## Working with Translations

Borsdata provides data in multiple languages:

```python
from borsdata_client import BorsdataClient

with BorsdataClient("your_api_key_here") as client:
    # Get translation metadata
    translations = client.get_translation_metadata()

    # Access translations for branches
    for branch in translations.branches[:5]:  # First 5 entries
        print(f"ID: {branch.id}")
        print(f"Swedish Name: {branch.name_sv}")
        print(f"English Name: {branch.name_en}")
        print("---")
```

# BorsdataClient API Reference

This document provides a comprehensive reference for the `BorsdataClient` class.

## Class: BorsdataClient

```python
class BorsdataClient:
    """Client for interacting with the Borsdata API."""
```

### Constructor

```python
def __init__(self, api_key: str):
    """Initialize the Borsdata API client.

    Args:
        api_key: Your Borsdata API key
    """
```

### Context Manager Support

The client can be used as a context manager:

```python
def __enter__(self):
    """Enter the context manager."""
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    """Exit the context manager."""
    # Cleanup resources
```

### Core Methods

#### \_get

```python
def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make a GET request to the Borsdata API.

    Args:
        endpoint: API endpoint path
        params: Optional query parameters

    Returns:
        API response as a dictionary

    Raises:
        BorsdataClientError: If the request fails
    """
```

### Data Retrieval Methods

#### get_branches

```python
def get_branches(self) -> List[Branch]:
    """Get all branches/industries.

    Returns:
        List of Branch objects
    """
```

#### get_countries

```python
def get_countries(self) -> List[Country]:
    """Get all countries.

    Returns:
        List of Country objects
    """
```

#### get_markets

```python
def get_markets(self) -> List[Market]:
    """Get all markets.

    Returns:
        List of Market objects
    """
```

#### get_instruments

```python
def get_instruments(self) -> List[Instrument]:
    """Get all Nordic instruments.

    Returns:
        List of Instrument objects
    """
```

#### get_global_instruments

```python
def get_global_instruments(self) -> List[Instrument]:
    """Get all global instruments.

    Note:
        Requires Pro+ subscription

    Returns:
        List of Instrument objects
    """
```

#### get_stock_prices

```python
def get_stock_prices(
    self,
    instrument_id: int,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    max_count: int = 20
) -> List[StockPrice]:
    """Get stock prices for an instrument.

    Args:
        instrument_id: Instrument ID
        from_date: Start date (optional)
        to_date: End date (optional)
        max_count: Maximum number of results (default: 20)

    Returns:
        List of StockPrice objects
    """
```

#### get_reports

```python
def get_reports(
    self,
    instrument_id: int,
    report_type: str = "year",
    max_count: int = 10,
    original_currency: bool = False
) -> List[Report]:
    """Get financial reports for an instrument.

    Args:
        instrument_id: Instrument ID
        report_type: Report type ("year", "quarter", "r12")
        max_count: Maximum number of results (default: 10)
        original_currency: Whether to use original currency (default: False)

    Returns:
        List of Report objects
    """
```

#### get_kpi_metadata

```python
def get_kpi_metadata(self) -> List[KpiMetadata]:
    """Get metadata for all KPIs.

    Returns:
        List of KpiMetadata objects
    """
```

#### get_insider_holdings

```python
def get_insider_holdings(self, instrument_ids: List[int]) -> List[InsiderListResponse]:
    """Get insider holdings for instruments.

    Args:
        instrument_ids: List of instrument IDs

    Returns:
        List of InsiderListResponse objects
    """
```

#### get_short_positions

```python
def get_short_positions(self) -> List[ShortsListResponse]:
    """Get short positions for all instruments.

    Returns:
        List of ShortsListResponse objects
    """
```

#### get_buybacks

```python
def get_buybacks(self, instrument_ids: List[int]) -> List[BuybackListResponse]:
    """Get buybacks for instruments.

    Args:
        instrument_ids: List of instrument IDs

    Returns:
        List of BuybackListResponse objects
    """
```

#### get_instrument_descriptions

```python
def get_instrument_descriptions(self, instrument_ids: List[int]) -> List[InstrumentDescriptionListResponse]:
    """Get descriptions for instruments.

    Args:
        instrument_ids: List of instrument IDs

    Returns:
        List of InstrumentDescriptionListResponse objects
    """
```

#### get_report_calendar

```python
def get_report_calendar(self, instrument_ids: List[int]) -> List[ReportCalendarListResponse]:
    """Get report calendar for instruments.

    Args:
        instrument_ids: List of instrument IDs

    Returns:
        List of ReportCalendarListResponse objects
    """
```

#### get_dividend_calendar

```python
def get_dividend_calendar(self, instrument_ids: List[int]) -> List[DividendCalendarListResponse]:
    """Get dividend calendar for instruments.

    Args:
        instrument_ids: List of instrument IDs

    Returns:
        List of DividendCalendarListResponse objects
    """
```

#### get_kpi_history

```python
def get_kpi_history(
    self,
    instrument_id: int,
    kpi_id: int,
    report_type: str,
    price_type: str = "mean",
    max_count: Optional[int] = None
) -> List[KpiAllResponse]:
    """Get KPI history for an instrument.

    Args:
        instrument_id: Instrument ID
        kpi_id: KPI ID
        report_type: Report type ("year", "quarter", "r12")
        price_type: Price type ("mean", "high", "low")
        max_count: Maximum number of results (optional)

    Returns:
        KpiAllResponse object
    """
```

#### get_kpi_updated

```python
def get_kpi_updated(self) -> datetime:
    """Get last update time for KPIs.

    Returns:
        Datetime of last KPI update
    """
```

#### get_last_stock_prices

```python
def get_last_stock_prices(self) -> List[StockPriceLastValue]:
    """Get last stock prices for all instruments.

    Returns:
        List of last stock prices
    """
```

#### get_last_global_stock_prices

```python
def get_last_global_stock_prices(self) -> List[StockPriceLastValue]:
    """Get last stock prices for all global instruments.

    Returns:
        List of last global stock prices
    """
```

#### get_stock_prices_by_date

```python
def get_stock_prices_by_date(self, date: datetime) -> List[StockPriceLastValue]:
    """Get stock prices for all instruments on a specific date.

    Args:
        date: The date to get prices for

    Returns:
        List of stock prices
    """
```

#### get_global_stock_prices_by_date

```python
def get_global_stock_prices_by_date(self, date: datetime) -> List[StockPriceLastValue]:
    """Get stock prices for all global instruments on a specific date.

    Args:
        date: The date to get prices for

    Returns:
        List of global stock prices
    """
```

#### get_stock_splits

```python
def get_stock_splits(self, from_date: Optional[datetime] = None) -> List[StockSplit]:
    """Get stock splits.

    Args:
        from_date: Start date (optional)

    Returns:
        List of StockSplit objects
    """
```

#### get_translation_metadata

```python
def get_translation_metadata(self) -> TranslationMetadataResponse:
    """Get translation metadata.

    Returns:
        TranslationMetadataResponse object
    """
```

## Class: BorsdataClientError

```python
class BorsdataClientError(Exception):
    """Exception raised for Borsdata API client errors."""
```

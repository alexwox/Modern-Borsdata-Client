"""Borsdata API Client - A modern Python client for the Borsdata API.

This package provides a clean, typed interface to the Borsdata API for financial data.

Example:
    >>> from borsdata_client import BorsdataClient
    >>> client = BorsdataClient("your_api_key")
    >>> instruments = client.get_instruments()
"""

from .client import BorsdataClient, BorsdataClientError
from .models import (
    Branch,
    BuybackRow,
    Country,
    DividendDate,
    InsiderRow,
    Instrument,
    InstrumentDescription,
    KpiMetadata,
    KpiValue,
    Market,
    Report,
    ReportCalendarDate,
    Sector,
    ShortPosition,
    StockPrice,
    StockPriceLastValue,
    StockSplit,
    TranslationItem,
)

__version__ = "0.1.0"
__all__ = [
    "BorsdataClient",
    "BorsdataClientError",
    "Instrument",
    "Branch",
    "Market",
    "Country",
    "Sector",
    "StockPrice",
    "Report",
    "KpiMetadata",
    "InsiderRow",
    "ShortPosition",
    "BuybackRow",
    "InstrumentDescription",
    "ReportCalendarDate",
    "DividendDate",
    "KpiValue",
    "StockPriceLastValue",
    "StockSplit",
    "TranslationItem",
]

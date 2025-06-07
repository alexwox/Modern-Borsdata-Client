"""Tests for the BorsdataClient API endpoints."""

import json
import os
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# from src.borsdata_client.client import BorsdataClient
from src.borsdata_client.models import (
    Branch,
    BuybackResponse,
    Country,
    DividendCalendarResponse,
    InsiderResponse,
    Instrument,
    InstrumentDescription,
    KpiAllResponse,
    KpiMetadata,
    KpisSummaryResponse,
    KpiSummaryGroup,
    Market,
    Report,
    ReportCalendarResponse,
    ShortsResponse,
    StockPrice,
    StockPriceLastValue,
    StockPricesArrayResp,
    StockPricesArrayRespList,
    StockSplit,
    TranslationMetadataResponse,
)

# Create fixtures directory if it doesn't exist
fixtures_dir = Path(__file__).parent / "fixtures"
fixtures_dir.mkdir(exist_ok=True)


def create_mock_response(endpoint: str, data: dict):
    """Create a mock response file for the given endpoint."""
    endpoint_parts = endpoint.strip("/").split("/")
    filename = "_".join(endpoint_parts) + ".json"

    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)

    fixture_path = fixtures_dir / filename
    with open(fixture_path, "w") as f:
        json.dump(data, f)

    # Print for debugging
    print(f"Created mock response file: {fixture_path}")
    print(f"Data: {data}")


# Test for get_branches
def test_get_branches(mock_client):
    """Test the get_branches method."""
    # Create mock response
    create_mock_response(
        "branches",
        {
            "branches": [
                {"id": 1, "name": "Test Branch 1", "sectorId": 10},
                {"id": 2, "name": "Test Branch 2", "sectorId": 20},
            ]
        },
    )

    # Call the method
    branches = mock_client.get_branches()

    # Verify the result
    assert len(branches) == 2
    assert isinstance(branches[0], Branch)
    assert branches[0].id == 1
    assert branches[0].name == "Test Branch 1"
    assert branches[0].sector_id == 10


# Test for get_countries
def test_get_countries(mock_client):
    """Test the get_countries method."""
    # Create mock response
    create_mock_response(
        "countries",
        {
            "countries": [
                {"id": 1, "name": "Test Country 1"},
                {"id": 2, "name": "Test Country 2"},
            ]
        },
    )

    # Call the method
    countries = mock_client.get_countries()

    # Verify the result
    assert len(countries) == 2
    assert isinstance(countries[0], Country)
    assert countries[0].id == 1
    assert countries[0].name == "Test Country 1"


# Test for get_markets
def test_get_markets(mock_client):
    """Test the get_markets method."""
    # Create mock response
    create_mock_response(
        "markets",
        {
            "markets": [
                {
                    "id": 1,
                    "name": "Test Market 1",
                    "countryId": 10,
                    "isIndex": False,
                    "exchangeName": "Exchange 1",
                },
                {
                    "id": 2,
                    "name": "Test Market 2",
                    "countryId": 20,
                    "isIndex": True,
                    "exchangeName": "Exchange 2",
                },
            ]
        },
    )

    # Call the method
    markets = mock_client.get_markets()

    # Verify the result
    assert len(markets) == 2
    assert isinstance(markets[0], Market)
    assert markets[0].id == 1
    assert markets[0].name == "Test Market 1"
    assert markets[0].country_id == 10
    assert markets[0].is_index is False
    assert markets[0].exchange_name == "Exchange 1"


def test_get_sectors(mock_client):
    """Test the get_sectors method."""
    # Create mock response
    create_mock_response(
        "sectors",
        {
            "sectors": [
                {"id": 10, "name": "Test Sector 1"},
                {"id": 20, "name": "Test Sector 2"},
            ]
        },
    )

    # Call the method
    sectors = mock_client.get_sectors()

    # Verify the result
    assert len(sectors) == 2
    assert sectors[0].id == 10
    assert sectors[0].name == "Test Sector 1"


# Test for get_instruments
def test_get_instruments(mock_client):
    """Test the get_instruments method."""
    # Create mock response
    create_mock_response(
        "instruments",
        {
            "instruments": [
                {
                    "insId": 1,
                    "name": "Test Instrument 1",
                    "urlName": "test-instrument-1",
                    "instrument": 1,
                    "isin": "SE0001234567",
                    "ticker": "TEST1",
                    "yahoo": "TEST1.ST",
                    "sectorId": 10,
                    "marketId": 1,
                    "branchId": 5,
                    "countryId": 2,
                    "listingDate": "2020-01-01",
                    "stockPriceCurrency": "SEK",
                    "reportCurrency": "SEK",
                }
            ]
        },
    )

    # Call the method
    instruments = mock_client.get_instruments()

    # Verify the result
    assert len(instruments) == 1
    assert isinstance(instruments[0], Instrument)
    assert instruments[0].ins_id == 1
    assert instruments[0].name == "Test Instrument 1"
    assert instruments[0].ticker == "TEST1"


# Test for get_global_instruments
def test_get_global_instruments(mock_client):
    """Test the get_global_instruments method."""
    # Create mock response
    create_mock_response(
        "instruments/global",
        {
            "instruments": [
                {
                    "insId": 1001,
                    "name": "Global Instrument 1",
                    "urlName": "global-instrument-1",
                    "instrument": 1,
                    "isin": "US1234567890",
                    "ticker": "GLOBAL1",
                    "yahoo": "GLOBAL1",
                    "sectorId": 10,
                    "marketId": 1,
                    "branchId": 5,
                    "countryId": 2,
                    "listingDate": "2020-01-01",
                    "stockPriceCurrency": "USD",
                    "reportCurrency": "USD",
                }
            ]
        },
    )

    # Call the method
    instruments = mock_client.get_global_instruments()

    # Verify the result
    assert len(instruments) == 1
    assert isinstance(instruments[0], Instrument)
    assert instruments[0].ins_id == 1001
    assert instruments[0].name == "Global Instrument 1"
    assert instruments[0].ticker == "GLOBAL1"


# Test for get_stock_prices
def test_get_stock_prices(mock_client):
    """Test the get_stock_prices method."""
    # Create mock response
    create_mock_response(
        "instruments/1/stockprices",
        {
            "instrument": 1,
            "stockPricesList": [
                {
                    "d": "2023-01-01",
                    "h": 100.5,
                    "l": 99.0,
                    "c": 100.0,
                    "o": 99.5,
                    "v": 10000,
                },
                {
                    "d": "2023-01-02",
                    "h": 101.5,
                    "l": 100.0,
                    "c": 101.0,
                    "o": 100.5,
                    "v": 12000,
                },
            ],
        },
    )

    # Call the method
    prices = mock_client.get_stock_prices(instrument_id=1)

    # Verify the result
    assert len(prices) == 2
    assert isinstance(prices[0], StockPrice)
    assert prices[0].d == "2023-01-01"
    assert prices[0].h == 100.5
    assert prices[0].c == 100.0


def test_get_stock_prices_batch(mock_client):
    """Test the get_stock_prices_batch method."""
    # Create mock response
    create_mock_response(
        "instruments/stockprices",
        {
            "stockPricesArrayList": [
                {
                    "instrument": 1,
                    "stockPricesList": [
                        {
                            "d": "2023-01-01",
                            "h": 100.5,
                            "l": 99.0,
                            "c": 100.0,
                            "o": 99.5,
                            "v": 10000,
                        }
                    ],
                },
                {
                    "instrument": 2,
                    "stockPricesList": [
                        {
                            "d": "2023-01-02",
                            "h": 101.5,
                            "l": 100.0,
                            "c": 101.0,
                            "o": 100.5,
                            "v": 12000,
                        }
                    ],
                },
            ]
        },
    )

    # Call the method
    prices = mock_client.get_stock_prices_batch(instrument_ids=[1, 2])

    # Verify the result
    assert len(prices) == 2
    assert isinstance(prices[0], StockPricesArrayRespList)
    assert prices[0].instrument == 1
    assert prices[0].stockPricesList[0].d == "2023-01-01"
    assert prices[0].stockPricesList[0].h == 100.5
    assert prices[0].stockPricesList[0].c == 100.0


# Test for get_reports
def test_get_reports(mock_client):
    """Test the get_reports method."""
    # Create mock response
    create_mock_response(
        "instruments/1/reports/year",
        {
            "instrument": 1,
            "reports": [
                {
                    "year": 2020,
                    "period": 1,
                    "revenues": 1000,
                    "gross_Income": 800.0,
                    "operating_Income": 600.0,
                    "profit_Before_Tax": 500.0,
                    "profit_To_Equity_Holders": 400.0,
                    "earnings_Per_Share": 2.0,
                    "number_Of_Shares": 200.0,
                    "dividend": 1.0,
                    "intangible_Assets": 300.0,
                    "tangible_Assets": 400.0,
                    "financial_Assets": 500.0,
                    "non_Current_Assets": 1200.0,
                    "cash_And_Equivalents": 200.0,
                    "current_Assets": 1500.0,
                    "total_Assets": 3000.0,
                    "total_Equity": 1800.0,
                    "non_Current_Liabilities": 700.0,
                    "current_Liabilities": 500.0,
                    "total_Liabilities_And_Equity": 3000.0,
                    "net_Debt": 100.0,
                    "cash_Flow_From_Operating_Activities": 600.0,
                    "cash_Flow_From_Investing_Activities": -200.0,
                    "cash_Flow_From_Financing_Activities": -100.0,
                    "cash_Flow_For_The_Year": 300.0,
                    "free_Cash_Flow": 400.0,
                    "stock_Price_Average": 50.0,
                    "stock_Price_High": 60.0,
                    "stock_Price_Low": 40.0,
                    "report_Start_Date": "2020-01-01T00:00:00",
                    "report_End_Date": "2020-12-31T00:00:00",
                    "broken_Fiscal_Year": False,
                    "currency": "USD",
                    "currency_Ratio": 1.0,
                    "net_Sales": 950.0,
                    "report_Date": "2021-01-31T00:00:00",
                }
            ],
        },
    )

    # Call the method
    reports = mock_client.get_reports(instrument_id=1)

    # Verify the result
    assert len(reports) == 1
    assert isinstance(reports[0], Report)
    assert reports[0].year == 2020
    assert reports[0].revenues == 1000
    assert reports[0].earnings_per_share == 2


# Test for get_kpi_metadata
def test_get_kpi_metadata(mock_client):
    """Test the get_kpi_metadata method."""
    # Create mock response with the correct key
    create_mock_response(
        "instruments/kpis/metadata",
        {
            "kpiHistoryMetadatas": [
                {
                    "kpiId": 1,
                    "nameSv": "KPI 1 (SV)",
                    "nameEn": "KPI 1 (EN)",
                    "format": "0.00",
                    "isString": False,
                },
                {
                    "kpiId": 2,
                    "nameSv": "KPI 2 (SV)",
                    "nameEn": "KPI 2 (EN)",
                    "format": "0.00%",
                    "isString": False,
                },
            ]
        },
    )

    # Call the method
    kpis = mock_client.get_kpi_metadata()

    # Verify the result
    assert len(kpis) == 2
    assert isinstance(kpis[0], KpiMetadata)
    assert kpis[0].kpi_id == 1
    assert kpis[0].name_en == "KPI 1 (EN)"
    assert kpis[0].is_string is False


# Test for get_insider_holdings
def test_get_insider_holdings(mock_client):
    """Test the get_insider_holdings method."""
    # Create mock response with the correct path
    create_mock_response(
        "holdings/insider",
        {
            "list": [
                {
                    "insId": 1,
                    "values": [
                        {
                            "misc": False,
                            "ownerName": "Test Owner",
                            "ownerPosition": "CEO",
                            "equityProgram": False,
                            "shares": 10000,
                            "price": 100.0,
                            "amount": 1000000.0,
                            "currency": "SEK",
                            "transactionType": 1,
                            "verificationDate": "2023-01-01T12:00:00",
                            "transactionDate": "2023-01-01T10:00:00",
                        }
                    ],
                    "error": None,
                }
            ]
        },
    )

    # Call the method
    insiders = mock_client.get_insider_holdings(instrument_ids=[1])

    # Verify the result
    assert len(insiders) == 1
    assert isinstance(insiders[0], InsiderResponse)
    assert insiders[0].ins_id == 1
    assert len(insiders[0].values) == 1
    assert insiders[0].values[0].owner_name == "Test Owner"


# Test for get_short_positions
def test_get_short_positions(mock_client):
    """Test the get_short_positions method."""
    # Create mock response with the correct path
    create_mock_response(
        "holdings/shorts",
        {
            "list": [
                {
                    "insId": 1,
                    "values": [
                        {
                            "positionHolder": "Test Holder",
                            "position": 0.5,
                            "date": "2023-01-01T12:00:00",
                        }
                    ],
                    "error": None,
                }
            ]
        },
    )

    # Call the method
    shorts = mock_client.get_short_positions()

    # Verify the result
    assert len(shorts) == 1
    assert isinstance(shorts[0], ShortsResponse)
    assert shorts[0].ins_id == 1
    assert len(shorts[0].values) == 1
    assert shorts[0].values[0].position_holder == "Test Holder"


# Test for get_buybacks
def test_get_buybacks(mock_client):
    """Test the get_buybacks method."""
    # Create mock response with the correct path
    create_mock_response(
        "holdings/buyback",
        {
            "list": [
                {
                    "insId": 1,
                    "values": [
                        {
                            "change": 1000,
                            "changeProc": 0.01,
                            "price": 100.0,
                            "currency": "SEK",
                            "shares": 10000,
                            "sharesProc": 0.05,
                            "date": "2023-01-01T12:00:00",
                        }
                    ],
                    "error": None,
                }
            ]
        },
    )

    # Call the method
    buybacks = mock_client.get_buybacks(instrument_ids=[1])

    # Verify the result
    assert len(buybacks) == 1
    assert isinstance(buybacks[0], BuybackResponse)
    assert buybacks[0].ins_id == 1
    assert len(buybacks[0].values) == 1
    assert buybacks[0].values[0].change == 1000


# Test for get_instrument_descriptions
def test_get_instrument_descriptions(mock_client):
    """Test the get_instrument_descriptions method."""
    # Create mock response with the correct path
    create_mock_response(
        "instruments/description",
        {
            "list": [
                {
                    "insId": 1,
                    "languageCode": "en",
                    "text": "Test description",
                    "error": None,
                }
            ]
        },
    )

    # Call the method
    descriptions = mock_client.get_instrument_descriptions(instrument_ids=[1])

    # Verify the result
    assert len(descriptions) == 1
    assert isinstance(descriptions[0], InstrumentDescription)
    assert descriptions[0].ins_id == 1
    assert descriptions[0].text == "Test description"


# Test for get_report_calendar
def test_get_report_calendar(mock_client):
    """Test the get_report_calendar method."""
    # Create mock response with the correct path
    create_mock_response(
        "instruments/report/calendar",
        {
            "list": [
                {
                    "insId": 1,
                    "values": [
                        {"releaseDate": "2023-04-01T08:00:00", "reportType": "Q1"}
                    ],
                    "error": None,
                }
            ]
        },
    )

    # Call the method
    calendar = mock_client.get_report_calendar(instrument_ids=[1])

    # Verify the result
    assert len(calendar) == 1
    assert isinstance(calendar[0], ReportCalendarResponse)
    assert calendar[0].ins_id == 1
    assert len(calendar[0].values) == 1
    assert calendar[0].values[0].report_type == "Q1"


# Test for get_dividend_calendar
def test_get_dividend_calendar(mock_client):
    """Test the get_dividend_calendar method."""
    # Create mock response with the correct path
    create_mock_response(
        "instruments/dividend/calendar",
        {
            "list": [
                {
                    "insId": 1,
                    "values": [
                        {
                            "amountPaid": 1.5,
                            "currencyShortName": "SEK",
                            "distributionFrequency": 1,
                            "excludingDate": "2023-04-15T00:00:00",
                            "dividendType": 1,
                        }
                    ],
                    "error": None,
                }
            ]
        },
    )

    # Call the method
    calendar = mock_client.get_dividend_calendar(instrument_ids=[1])

    # Verify the result
    assert len(calendar) == 1
    assert isinstance(calendar[0], DividendCalendarResponse)
    assert calendar[0].ins_id == 1
    assert len(calendar[0].values) == 1
    assert calendar[0].values[0].dividend_type == 1


# Test for get_kpi_history
def test_get_kpi_history(mock_client):
    """Test the get_kpi_history method."""
    # Create mock response
    create_mock_response(
        "instruments/1/kpis/2/year/mean/history",
        {
            "kpiId": 2,
            "group": "Test Group",
            "calculation": "Test Calculation",
            "values": [{"i": 1, "n": 10.5, "s": None}, {"i": 1, "n": 11.2, "s": None}],
        },
    )

    # Call the method
    kpi_history = mock_client.get_kpi_history(
        instrument_id=1, kpi_id=2, report_type="year"
    )

    # Verify the result
    assert isinstance(kpi_history, KpiAllResponse)
    assert kpi_history.kpi_id == 2
    assert kpi_history.group == "Test Group"
    assert len(kpi_history.values) == 2
    assert kpi_history.values[0].i == 1
    assert kpi_history.values[0].n == 10.5


def test_get_kpi_summary(mock_client):
    """Test the get_kpi_summary method."""
    # Create mock response
    create_mock_response(
        "instruments/1/kpis/year/summary",
        {
            "instrument": 2,
            "reportType": "year",
            "kpis": [
                {
                    "KpiId": 2,
                    "values": [
                        {"y": 1, "p": 10, "v": None},
                        {"y": 2, "p": 20, "v": 10},
                    ],
                }
            ],
        },
    )

    # Call the method
    kpi_summary = mock_client.get_kpi_summary(
        instrument_id=1, report_type="year", max_count=2
    )

    # Verify the result
    assert isinstance(kpi_summary, list)
    assert isinstance(kpi_summary[0], KpiSummaryGroup)
    assert kpi_summary[0].kpi_id == 2
    assert len(kpi_summary[0].values) == 2
    assert kpi_summary[0].values[0].year == 1
    assert kpi_summary[0].values[0].value is None
    assert kpi_summary[0].values[1].period == 20


# Test for get_kpi_updated
def test_get_kpi_updated(mock_client):
    """Test the get_kpi_updated method."""
    # Create mock response
    create_mock_response(
        "instruments/kpis/updated", {"kpisCalcUpdated": "2023-01-15T12:30:45"}
    )

    # Call the method
    updated = mock_client.get_kpi_updated()

    # Verify the result
    assert isinstance(updated, datetime)
    assert updated.year == 2023
    assert updated.month == 1
    assert updated.day == 15


# Test for get_last_stock_prices
def test_get_last_stock_prices(mock_client):
    """Test the get_last_stock_prices method."""
    # Create mock response
    create_mock_response(
        "instruments/stockprices/last",
        {
            "stockPricesList": [
                {
                    "i": 1,
                    "d": "2023-01-15",
                    "h": 105.5,
                    "l": 103.0,
                    "c": 104.0,
                    "o": 103.5,
                    "v": 15000,
                },
                {
                    "i": 2,
                    "d": "2023-01-15",
                    "h": 205.5,
                    "l": 203.0,
                    "c": 204.0,
                    "o": 203.5,
                    "v": 25000,
                },
            ]
        },
    )

    # Call the method
    prices = mock_client.get_last_stock_prices()

    # Verify the result
    assert len(prices) == 2
    assert isinstance(prices[0], StockPriceLastValue)
    assert prices[0].i == 1
    assert prices[0].d == "2023-01-15"
    assert prices[0].c == 104.0


# Test for get_last_global_stock_prices
def test_get_last_global_stock_prices(mock_client):
    """Test the get_last_global_stock_prices method."""
    # Create mock response
    create_mock_response(
        "instruments/stockprices/global/last",
        {
            "stockPricesList": [
                {
                    "i": 1001,
                    "d": "2023-01-15",
                    "h": 305.5,
                    "l": 303.0,
                    "c": 304.0,
                    "o": 303.5,
                    "v": 35000,
                }
            ]
        },
    )

    # Call the method
    prices = mock_client.get_last_global_stock_prices()

    # Verify the result
    assert len(prices) == 1
    assert isinstance(prices[0], StockPriceLastValue)
    assert prices[0].i == 1001
    assert prices[0].c == 304.0


# Test for get_stock_prices_by_date
def test_get_stock_prices_by_date(mock_client):
    """Test the get_stock_prices_by_date method."""
    # Create mock response with the correct path
    test_date = datetime(2023, 1, 15)
    create_mock_response(
        "instruments/stockprices/date",
        {
            "stockPricesList": [
                {
                    "i": 1,
                    "d": "2023-01-15",
                    "h": 105.5,
                    "l": 103.0,
                    "c": 104.0,
                    "o": 103.5,
                    "v": 15000,
                }
            ]
        },
    )

    # Call the method
    prices = mock_client.get_stock_prices_by_date(date=test_date)

    # Verify the result
    assert len(prices) == 1
    assert isinstance(prices[0], StockPriceLastValue)
    assert prices[0].i == 1
    assert prices[0].d == "2023-01-15"
    assert prices[0].c == 104.0


# Test for get_global_stock_prices_by_date
def test_get_global_stock_prices_by_date(mock_client):
    """Test the get_global_stock_prices_by_date method."""
    # Create mock response with the correct path
    test_date = datetime(2023, 1, 15)
    create_mock_response(
        "instruments/stockprices/global/date",
        {
            "stockPricesList": [
                {
                    "i": 1001,
                    "d": "2023-01-15",
                    "h": 305.5,
                    "l": 303.0,
                    "c": 304.0,
                    "o": 303.5,
                    "v": 35000,
                }
            ]
        },
    )

    # Call the method
    prices = mock_client.get_global_stock_prices_by_date(date=test_date)

    # Verify the result
    assert len(prices) == 1
    assert isinstance(prices[0], StockPriceLastValue)
    assert prices[0].i == 1001
    assert prices[0].d == "2023-01-15"
    assert prices[0].c == 304.0


# Test for get_stock_splits
def test_get_stock_splits(mock_client):
    """Test the get_stock_splits method."""
    # Create mock response
    create_mock_response(
        "instruments/stocksplits",
        {
            "stockSplits": [
                {
                    "insId": 1,
                    "splitDate": "2023-01-15T00:00:00",
                    "splitRatio": 2.0,
                    "splitType": "split",
                },
                {
                    "insId": 2,
                    "splitDate": "2023-02-15T00:00:00",
                    "splitRatio": 0.5,
                    "splitType": "reverse",
                },
            ]
        },
    )

    # Call the method
    splits = mock_client.get_stock_splits()

    # Verify the result
    assert len(splits) == 2
    assert isinstance(splits[0], StockSplit)
    assert splits[0].ins_id == 1
    assert splits[0].split_ratio == 2.0
    assert splits[0].split_type == "split"


# Test for get_translation_metadata
def test_get_translation_metadata(mock_client):
    """Test the get_translation_metadata method."""
    # Create mock response with the correct path
    create_mock_response(
        "translationmetadata",
        {
            "translationMetadatas": [
                {
                    "nameSv": "Branch 1 (SV)",
                    "nameEn": "Branch 1 (EN)",
                    "translationKey": "L_BRANCH_1",
                },
                {
                    "nameSv": "Sector 1 (SV)",
                    "nameEn": "Sector 1 (EN)",
                    "translationKey": "L_SECTOR_10",
                },
                {
                    "nameSv": "Country 1 (SV)",
                    "nameEn": "Country 1 (EN)",
                    "translationKey": "L_COUNTRY_2",
                },
            ]
        },
    )

    # Call the method
    translations = mock_client.get_translation_metadata()

    # Verify the result
    assert isinstance(translations, TranslationMetadataResponse)
    assert len(translations.branches) > 0
    assert translations.branches[0].id == 1
    assert translations.branches[0].name_sv == "Branch 1 (SV)"
    assert len(translations.sectors) > 0
    assert translations.sectors[0].id == 10
    assert len(translations.countries) > 0
    assert translations.countries[0].id == 2

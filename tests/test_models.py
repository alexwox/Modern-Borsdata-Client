"""Tests for the Pydantic models used in the BorsdataClient."""

from datetime import datetime
from typing import List, Optional

import pytest

from borsdata_client.models import (
    Branch,
    BranchesResponse,
    BuybackListResponse,
    BuybackResponse,
    BuybackRow,
    CountriesResponse,
    Country,
    DividendCalendarListResponse,
    DividendCalendarResponse,
    DividendDate,
    InsiderListResponse,
    InsiderResponse,
    InsiderRow,
    Instrument,
    InstrumentDescription,
    InstrumentDescriptionListResponse,
    InstrumentsResponse,
    KpiAllResponse,
    KpiCalcUpdatedResponse,
    KpiHistory,
    KpiMetadata,
    KpisHistoryArrayResp,
    KpisHistoryComp,
    KpisSummaryResponse,
    KpiSummaryGroup,
    KpiSummaryValue,
    KpiValue,
    Market,
    MarketsResponse,
    Report,
    ReportCalendarDate,
    ReportCalendarListResponse,
    ReportCalendarResponse,
    Sector,
    SectorsResponse,
    ShortPosition,
    ShortsListResponse,
    ShortsResponse,
    StockPrice,
    StockPriceLastResponse,
    StockPriceLastValue,
    StockPricesResponse,
    StockSplit,
    StockSplitResponse,
    TranslationItem,
    TranslationMetadataResponse,
)


def test_branch_model():
    """Test the Branch model."""
    data = {"id": 1, "name": "Test Branch", "sectorId": 10}
    branch = Branch(**data)
    assert branch.id == 1
    assert branch.name == "Test Branch"
    assert branch.sector_id == 10


def test_country_model():
    """Test the Country model."""
    data = {"id": 1, "name": "Test Country"}
    country = Country(**data)
    assert country.id == 1
    assert country.name == "Test Country"


def test_market_model():
    """Test the Market model."""
    data = {
        "id": 1,
        "name": "Test Market",
        "countryId": 10,
        "isIndex": True,
        "exchangeName": "Test Exchange",
    }
    market = Market(**data)
    assert market.id == 1
    assert market.name == "Test Market"
    assert market.country_id == 10
    assert market.is_index is True
    assert market.exchange_name == "Test Exchange"


def test_sector_model():
    """Test the Sector model."""
    data = {"id": 1, "name": "Test Sector"}
    sector = Sector(**data)
    assert sector.id == 1
    assert sector.name == "Test Sector"


def test_sectors_response_model():
    """Test the SectorsResponse model."""
    data = {
        "sectors": [
            {"id": 1, "name": "Test Sector 1"},
            {"id": 2, "name": "Test Sector 2"},
        ]
    }
    sectors_response = SectorsResponse(**data)
    assert len(sectors_response.sectors) == 2
    assert sectors_response.sectors[0].id == 1
    assert sectors_response.sectors[0].name == "Test Sector 1"
    assert sectors_response.sectors[1].id == 2
    assert sectors_response.sectors[1].name == "Test Sector 2"


def test_instrument_model():
    """Test the Instrument model."""
    data = {
        "insId": 1,
        "name": "Test Instrument",
        "urlName": "test-instrument",
        "instrument": 1,
        "isin": "SE0000000001",
        "ticker": "TEST",
        "yahoo": "TEST.ST",
        "sectorId": 1,
        "marketId": 1,
        "branchId": 1,
        "countryId": 1,
        "listingDate": "2020-01-01T00:00:00",
        "stockPriceCurrency": "SEK",
        "reportCurrency": "SEK",
    }
    instrument = Instrument(**data)
    assert instrument.ins_id == 1
    assert instrument.name == "Test Instrument"
    assert instrument.url_name == "test-instrument"
    assert instrument.instrument_type == 1
    assert instrument.isin == "SE0000000001"
    assert instrument.ticker == "TEST"
    assert instrument.yahoo_symbol == "TEST.ST"
    assert instrument.sector_id == 1
    assert instrument.market_id == 1
    assert instrument.branch_id == 1
    assert instrument.country_id == 1
    assert instrument.listing_date == datetime(2020, 1, 1, 0, 0, 0)
    assert instrument.stock_price_currency == "SEK"
    assert instrument.report_currency == "SEK"


def test_stock_price_model():
    """Test the StockPrice model."""
    data = {"d": "2020-01-01", "h": 100.0, "l": 90.0, "c": 95.0, "o": 92.0, "v": 1000}
    stock_price = StockPrice(**data)
    assert stock_price.d == "2020-01-01"
    assert stock_price.h == 100.0
    assert stock_price.l == 90.0
    assert stock_price.c == 95.0
    assert stock_price.o == 92.0
    assert stock_price.v == 1000

    # Test the get_date method
    assert stock_price.get_date() == datetime(2020, 1, 1)


def test_kpi_metadata_model():
    """Test the KpiMetadata model."""
    data = {
        "kpiId": 1,
        "nameSv": "Test KPI SV",
        "nameEn": "Test KPI EN",
        "format": "percent",
        "isString": False,
    }
    kpi_metadata = KpiMetadata(**data)
    assert kpi_metadata.kpi_id == 1
    assert kpi_metadata.name_sv == "Test KPI SV"
    assert kpi_metadata.name_en == "Test KPI EN"
    assert kpi_metadata.format == "percent"
    assert kpi_metadata.is_string is False


def test_kpi_summary_group_model():
    """Test the KpiSummaryGroup model."""
    data = {
        "KpiId": 1,
        "values": [],
    }
    kpi_summary_group = KpiSummaryGroup(**data)
    assert kpi_summary_group.kpi_id == 1
    assert isinstance(kpi_summary_group.values, list)


def test_kpi_summary_value_model():
    """Test the KpiSummaryValue model."""
    data = {
        "y": 2020,
        "p": 1,
        "v": 100.0,
    }
    kpi_summary_value = KpiSummaryValue(**data)
    assert kpi_summary_value.year == 2020
    assert kpi_summary_value.period == 1
    assert kpi_summary_value.value == 100.0


def test_kpi_summary_response_model():
    """Test the KpiSummaryResponse model."""
    data = {
        "instrument": 1,
        "reportType": "Test Year",
        "kpis": [
            {
                "KpiId": 1,
                "values": [
                    {
                        "y": 2020,
                        "p": 1,
                        "v": 100.0,
                    }
                ],
            }
        ],
    }
    kpi_summary_response = KpisSummaryResponse(**data)
    assert kpi_summary_response.instrument == 1
    assert kpi_summary_response.report_type == "Test Year"
    assert len(kpi_summary_response.kpis) == 1
    assert kpi_summary_response.kpis[0].kpi_id == 1
    assert kpi_summary_response.kpis[0].values[0].year == 2020
    assert kpi_summary_response.kpis[0].values[0].period == 1
    assert kpi_summary_response.kpis[0].values[0].value == 100.0


def test_kpi_value_model():
    """Test the KpiValue model."""
    data = {
        "year": 2020,
        "period": 1,
        "value": 100.0,
    }
    kpi_value = KpiValue(**data)
    assert kpi_value.year == 2020
    assert kpi_value.period == 1
    assert kpi_value.value == 100.0


def test_kpi_history_model():
    """Test the KpiHistory model."""
    data = {
        "y": 2020,
        "p": 1,
        "v": 100.0,
    }
    kpi_history = KpiHistory(**data)
    assert kpi_history.year == 2020
    assert kpi_history.y == 2020
    assert kpi_history.period == 1
    assert kpi_history.p == 1
    assert kpi_history.value == 100.0
    assert kpi_history.v == 100.0


def test_kpis_history_array_resp_model():
    """Test the KpisHistoryArrayResp model."""
    data = {
        "kpiId": 1,
        "priceValue": "mean",
        "reportTime": "2021-01-01",
        "kpisList": [
            {
                "instrument": 1,
                "kpi_id": None,
                "error": None,
                "values": [
                    {"y": 2020, "p": 1, "v": 100.0},
                    {"y": 2020, "p": 2, "v": 200.0},
                ],
            }
        ],
    }
    kpis_history_array_resp = KpisHistoryArrayResp(**data)
    assert kpis_history_array_resp.kpi_id == 1
    assert kpis_history_array_resp.price_value == "mean"
    assert len(kpis_history_array_resp.kpis_list) == 1
    assert kpis_history_array_resp.kpis_list[0].kpi_id is None
    assert kpis_history_array_resp.kpis_list[0].instrument == 1
    assert len(kpis_history_array_resp.kpis_list[0].values) == 2


def test_report_model():
    """Test the Report model."""
    data = {
        "year": 2020,
        "period": 1,
        "revenues": 1000.0,
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
    report = Report(**data)
    assert report.year == 2020
    assert report.period == 1
    assert report.revenues == 1000.0
    assert report.gross_income == 800.0
    assert report.operating_income == 600.0
    assert report.profit_before_tax == 500.0
    assert report.profit_to_equity_holders == 400.0
    assert report.earnings_per_share == 2.0
    assert report.number_of_shares == 200.0
    assert report.dividend == 1.0
    assert report.intangible_assets == 300.0
    assert report.tangible_assets == 400.0
    assert report.financial_assets == 500.0
    assert report.non_current_assets == 1200.0
    assert report.cash_and_equivalents == 200.0
    assert report.current_assets == 1500.0
    assert report.total_assets == 3000.0
    assert report.total_equity == 1800.0
    assert report.non_current_liabilities == 700.0
    assert report.current_liabilities == 500.0
    assert report.total_liabilities_and_equity == 3000.0
    assert report.net_debt == 100.0
    assert report.cash_flow_from_operating_activities == 600.0
    assert report.cash_flow_from_investing_activities == -200.0
    assert report.cash_flow_from_financing_activities == -100.0
    assert report.cash_flow_for_the_year == 300.0
    assert report.free_cash_flow == 400.0
    assert report.stock_price_average == 50.0
    assert report.stock_price_high == 60.0
    assert report.stock_price_low == 40.0
    assert report.report_start_date == datetime(2020, 1, 1)
    assert report.report_end_date == datetime(2020, 12, 31)
    assert report.broken_fiscal_year is False
    assert report.currency == "USD"
    assert report.currency_ratio == 1.0
    assert report.net_sales == 950.0
    assert report.report_date == datetime(2021, 1, 31)


def test_insider_row_model():
    """Test the InsiderRow model."""
    data = {
        "misc": False,
        "ownerName": "Test Owner",
        "ownerPosition": "CEO",
        "equityProgram": False,
        "shares": 1000,
        "price": 100.0,
        "amount": 100000.0,
        "currency": "SEK",
        "transactionType": 1,
        "verificationDate": "2020-01-01T00:00:00",
        "transactionDate": "2020-01-01T00:00:00",
    }
    insider_row = InsiderRow(**data)
    assert insider_row.misc is False
    assert insider_row.owner_name == "Test Owner"
    assert insider_row.owner_position == "CEO"
    assert insider_row.equity_program is False
    assert insider_row.shares == 1000
    assert insider_row.price == 100.0
    assert insider_row.amount == 100000.0
    assert insider_row.currency == "SEK"
    assert insider_row.transaction_type == 1
    assert insider_row.verification_date == datetime(2020, 1, 1, 0, 0, 0)
    assert insider_row.transaction_date == datetime(2020, 1, 1, 0, 0, 0)


def test_insider_response_model():
    """Test the InsiderResponse model."""
    data = {
        "insId": 1,
        "values": [
            {
                "misc": False,
                "ownerName": "Test Owner",
                "ownerPosition": "CEO",
                "equityProgram": False,
                "shares": 1000,
                "price": 100.0,
                "amount": 100000.0,
                "currency": "SEK",
                "transactionType": 1,
                "verificationDate": "2020-01-01T00:00:00",
                "transactionDate": "2020-01-01T00:00:00",
            }
        ],
        "error": None,
    }
    insider_response = InsiderResponse(**data)
    assert insider_response.ins_id == 1
    assert len(insider_response.values) == 1
    assert insider_response.values[0].owner_name == "Test Owner"
    assert insider_response.error is None


def test_insider_list_response_model():
    """Test the InsiderListResponse model."""
    data = {
        "list": [
            {
                "insId": 1,
                "values": [
                    {
                        "misc": False,
                        "ownerName": "Test Owner",
                        "ownerPosition": "CEO",
                        "equityProgram": False,
                        "shares": 1000,
                        "price": 100.0,
                        "amount": 100000.0,
                        "currency": "SEK",
                        "transactionType": 1,
                        "verificationDate": "2020-01-01T00:00:00",
                        "transactionDate": "2020-01-01T00:00:00",
                    }
                ],
                "error": None,
            }
        ]
    }
    insider_list_response = InsiderListResponse(**data)
    assert len(insider_list_response.list) == 1
    assert insider_list_response.list[0].ins_id == 1
    assert len(insider_list_response.list[0].values) == 1


def test_stock_price_last_value_model():
    """Test the StockPriceLastValue model."""
    data = {
        "i": 1,
        "d": "2020-01-01",
        "h": 100.0,
        "l": 90.0,
        "c": 95.0,
        "o": 92.0,
        "v": 1000,
    }
    stock_price_last_value = StockPriceLastValue(**data)
    assert stock_price_last_value.i == 1
    assert stock_price_last_value.d == "2020-01-01"
    assert stock_price_last_value.h == 100.0
    assert stock_price_last_value.l == 90.0
    assert stock_price_last_value.c == 95.0
    assert stock_price_last_value.o == 92.0
    assert stock_price_last_value.v == 1000


def test_stock_price_last_response_model():
    """Test the StockPriceLastResponse model."""
    data = {
        "stockPricesList": [
            {
                "i": 1,
                "d": "2020-01-01",
                "h": 100.0,
                "l": 90.0,
                "c": 95.0,
                "o": 92.0,
                "v": 1000,
            }
        ]
    }
    stock_price_last_response = StockPriceLastResponse(**data)
    assert len(stock_price_last_response.values) == 1
    assert stock_price_last_response.values[0].i == 1
    assert stock_price_last_response.values[0].d == "2020-01-01"


def test_kpi_value_model():
    """Test the KpiValue model."""
    data = {"i": 1, "n": 100.0, "s": "Test"}
    kpi_value = KpiValue(**data)
    assert kpi_value.i == 1
    assert kpi_value.n == 100.0
    assert kpi_value.s == "Test"


def test_kpi_all_response_model():
    """Test the KpiAllResponse model."""
    data = {
        "kpiId": 1,
        "group": "Test Group",
        "calculation": "Test Calculation",
        "values": [{"i": 1, "n": 100.0, "s": "Test"}],
    }
    kpi_all_response = KpiAllResponse(**data)
    assert kpi_all_response.kpi_id == 1
    assert kpi_all_response.group == "Test Group"
    assert kpi_all_response.calculation == "Test Calculation"
    assert len(kpi_all_response.values) == 1
    assert kpi_all_response.values[0].i == 1


def test_kpi_calc_updated_response_model():
    """Test the KpiCalcUpdatedResponse model."""
    data = {"kpisCalcUpdated": "2020-01-01T00:00:00"}
    kpi_calc_updated_response = KpiCalcUpdatedResponse(**data)
    assert kpi_calc_updated_response.kpis_calc_updated == datetime(2020, 1, 1, 0, 0, 0)


def test_stock_split_model():
    """Test the StockSplit model."""
    data = {
        "insId": 1,
        "splitDate": "2020-01-01T00:00:00",
        "splitRatio": 2.0,
        "splitType": "forward",
    }
    stock_split = StockSplit(**data)
    assert stock_split.ins_id == 1
    assert stock_split.split_date == datetime(2020, 1, 1, 0, 0, 0)
    assert stock_split.split_ratio == 2.0
    assert stock_split.split_type == "forward"


def test_stock_split_response_model():
    """Test the StockSplitResponse model."""
    data = {
        "stockSplits": [
            {
                "insId": 1,
                "splitDate": "2020-01-01T00:00:00",
                "splitRatio": 2.0,
                "splitType": "forward",
            }
        ]
    }
    stock_split_response = StockSplitResponse(**data)
    assert len(stock_split_response.stock_splits) == 1
    assert stock_split_response.stock_splits[0].ins_id == 1
    assert stock_split_response.stock_splits[0].split_ratio == 2.0


def test_translation_item_model():
    """Test the TranslationItem model."""
    data = {"id": 1, "nameSv": "Test SV", "nameEn": "Test EN"}
    translation_item = TranslationItem(**data)
    assert translation_item.id == 1
    assert translation_item.name_sv == "Test SV"
    assert translation_item.name_en == "Test EN"


def test_translation_metadata_response_model():
    """Test the TranslationMetadataResponse model."""
    data = {
        "translationMetadatas": [
            {
                "nameSv": "Test Branch SV",
                "nameEn": "Test Branch EN",
                "translationKey": "L_BRANCH_1",
            },
            {
                "nameSv": "Test Sector SV",
                "nameEn": "Test Sector EN",
                "translationKey": "L_SECTOR_1",
            },
            {
                "nameSv": "Test Country SV",
                "nameEn": "Test Country EN",
                "translationKey": "L_COUNTRY_1",
            },
        ]
    }
    translation_metadata_response = TranslationMetadataResponse(**data)

    # Debug prints
    print("Branches:", translation_metadata_response.branches)
    print("First branch:", translation_metadata_response.branches[0])
    print("First branch name_sv:", translation_metadata_response.branches[0].name_sv)
    print("First branch name_en:", translation_metadata_response.branches[0].name_en)
    print("First branch dict:", translation_metadata_response.branches[0].model_dump())

    assert len(translation_metadata_response.branches) == 1
    assert translation_metadata_response.branches[0].id == 1
    assert translation_metadata_response.branches[0].name_sv == "Test Branch SV"
    assert len(translation_metadata_response.sectors) == 1
    assert translation_metadata_response.sectors[0].id == 1
    assert translation_metadata_response.sectors[0].name_sv == "Test Sector SV"
    assert len(translation_metadata_response.countries) == 1
    assert translation_metadata_response.countries[0].id == 1
    assert translation_metadata_response.countries[0].name_sv == "Test Country SV"

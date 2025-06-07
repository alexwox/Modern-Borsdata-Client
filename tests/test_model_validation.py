"""Tests for model validation in the BorsdataClient."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.borsdata_client.models import (
    Branch,
    InsiderRow,
    Instrument,
    KpiMetadata,
    KpiSummaryGroup,
    Report,
    ReportMetadata,
    StockPrice,
    StockPriceLastValue,
    StockPricesArrayRespList,
    StockSplit,
)


def test_branch_validation():
    """Test that Branch model validates input data."""
    # Missing required field
    with pytest.raises(ValidationError):
        Branch(name="Test Branch")

    # Invalid type for id
    with pytest.raises(ValidationError):
        Branch(id="not_an_int", name="Test Branch", sectorId=1)

    # Valid data should not raise an error
    Branch(id=1, name="Test Branch", sectorId=1)


def test_instrument_validation():
    """Test that Instrument model validates input data."""
    # Missing required field
    with pytest.raises(ValidationError):
        Instrument(name="Test Instrument")

    # Invalid type for insId
    with pytest.raises(ValidationError):
        Instrument(insId="not_an_int", name="Test Instrument", instrument=1, marketId=1)

    # Invalid date format
    with pytest.raises(ValidationError):
        Instrument(
            insId=1,
            name="Test Instrument",
            instrument=1,
            marketId=1,
            urlName="test-instrument",
            isin="SE0000000001",
            ticker="TEST",
            yahoo="TEST.ST",
            listingDate="not_a_date",
        )

    # Valid data should not raise an error
    Instrument(
        insId=1,
        name="Test Instrument",
        instrument=1,
        marketId=1,
        urlName="test-instrument",
        isin="SE0000000001",
        ticker="TEST",
        yahoo="TEST.ST",
    )


def test_stock_price_validation():
    """Test that StockPrice model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        StockPrice(d="2020-01-01")

    # Invalid type for h (high price)
    with pytest.raises(ValidationError):
        StockPrice(d="2020-01-01", h="not_a_float", l=90.0, c=95.0, o=92.0, v=1000)

    # Valid data should not raise an error
    StockPrice(d="2020-01-01", h=100.0, l=90.0, c=95.0, o=92.0, v=1000)


def test_stock_prices_array_resp_list_validation():
    """Test that StockPricesArrayRespList model validates input data."""
    # Missing required field
    with pytest.raises(ValidationError):
        StockPricesArrayRespList()

    # Invalid type for stockPricesList
    with pytest.raises(ValidationError):
        StockPricesArrayRespList(stockPricesList="not_a_list")

    # Valid data should not raise an error
    StockPricesArrayRespList(
        instrument=1,
        stockPricesList=[
            StockPrice(d="2020-01-01", h=100.0, l=90.0, c=95.0, o=92.0, v=1000),
        ],
    )


def test_kpi_metadata_validation():
    """Test that KpiMetadata model validates input data."""
    # Missing required field
    with pytest.raises(ValidationError):
        KpiMetadata(nameSv="Test KPI")

    # Invalid type for kpiId
    with pytest.raises(ValidationError):
        KpiMetadata(
            kpiId="not_an_int", nameSv="Test KPI", isString=False, format="percent"
        )

    # Invalid type for isString
    with pytest.raises(ValidationError):
        KpiMetadata(kpiId=1, nameSv="Test KPI", isString="not_a_bool", format="percent")

    # Valid data should not raise an error
    KpiMetadata(kpiId=1, nameSv="Test KPI", isString=False, format="percent")


def test_kpi_summary_group_validation():
    """Test that KpiSummaryGroup model validates input data."""
    # Missing required field
    with pytest.raises(ValidationError):
        KpiSummaryGroup(KpiId="Test Group")

    # Invalid type for kpiId
    with pytest.raises(ValidationError):
        KpiSummaryGroup(KpiId="not_an_int", values=[])

    # Valid data should not raise an error
    KpiSummaryGroup(KpiId=1, values=[{"y": 2020, "p": 1, "v": 100}])


def test_report_validation():
    """Test that Report model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        Report(year=2020)

    # Invalid type for year
    with pytest.raises(ValidationError):
        Report(
            year="not_an_int",
            period=1,
            revenues=1000.0,
            operating_Income=100.0,
            profit_Before_Tax=80.0,
            earnings_Per_Share=2.0,
            number_Of_Shares=100.0,
            dividend=1.0,
            non_Current_Assets=200.0,
        )

    # Valid data should not raise an error
    Report(
        year=2020,
        period=1,
        revenues=1000.0,
        gross_Income=800.0,
        operating_Income=600.0,
        profit_Before_Tax=500.0,
        profit_To_Equity_Holders=400.0,
        earnings_Per_Share=2.0,
        number_Of_Shares=200.0,
        dividend=1.0,
        intangible_Assets=300.0,
        tangible_Assets=400.0,
        financial_Assets=500.0,
        non_Current_Assets=1200.0,
        cash_And_Equivalents=200.0,
        current_Assets=1500.0,
        total_Assets=3000.0,
        total_Equity=1800.0,
        non_Current_Liabilities=700.0,
        current_Liabilities=500.0,
        total_Liabilities_And_Equity=3000.0,
        net_Debt=100.0,
        cash_Flow_From_Operating_Activities=600.0,
        cash_Flow_From_Investing_Activities=-200.0,
        cash_Flow_From_Financing_Activities=-100.0,
        cash_Flow_For_The_Year=300.0,
        free_Cash_Flow=400.0,
        stock_Price_Average=50.0,
        stock_Price_High=60.0,
        stock_Price_Low=40.0,
        report_Start_Date="2020-01-01T00:00:00",
        report_End_Date="2020-12-31T00:00:00",
        broken_Fiscal_Year=False,
        currency="USD",
        currency_Ratio=1.0,
        net_Sales=950.0,
        report_Date="2021-01-31T00:00:00",
    )


def test_report_metadata_validation():
    """Test that ReportMetadata model validates input data."""

    # Invalid type for reportPropery
    with pytest.raises(ValidationError):
        ReportMetadata(reportPropery=1)

    # Valid data should not raise an error
    ReportMetadata()
    ReportMetadata(
        reportPropery="Test Property",
        nameSv="Test Name",
        nameEn="Test Name EN",
        format="Test Format",
    )


def test_insider_row_validation():
    """Test that InsiderRow model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        InsiderRow(misc=False)

    # Invalid type for shares
    with pytest.raises(ValidationError):
        InsiderRow(
            misc=False,
            ownerName="Test Owner",
            equityProgram=False,
            shares="not_an_int",
            price=100.0,
            amount=100000.0,
            currency="SEK",
            transactionType=1,
            verificationDate="2020-01-01T00:00:00",
        )

    # Invalid date format
    with pytest.raises(ValidationError):
        InsiderRow(
            misc=False,
            ownerName="Test Owner",
            equityProgram=False,
            shares=1000,
            price=100.0,
            amount=100000.0,
            currency="SEK",
            transactionType=1,
            verificationDate="not_a_date",
        )

    # Valid data should not raise an error
    InsiderRow(
        misc=False,
        ownerName="Test Owner",
        equityProgram=False,
        shares=1000,
        price=100.0,
        amount=100000.0,
        currency="SEK",
        transactionType=1,
        verificationDate="2020-01-01T00:00:00",
    )


def test_stock_price_last_value_validation():
    """Test that StockPriceLastValue model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        StockPriceLastValue(i=1)

    # Invalid type for i (instrument id)
    with pytest.raises(ValidationError):
        StockPriceLastValue(
            i="not_an_int", d="2020-01-01", h=100.0, l=90.0, c=95.0, o=92.0, v=1000
        )

    # Valid data should not raise an error
    StockPriceLastValue(i=1, d="2020-01-01", h=100.0, l=90.0, c=95.0, o=92.0, v=1000)


def test_stock_split_validation():
    """Test that StockSplit model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        StockSplit(insId=1)

    # Invalid type for splitRatio
    with pytest.raises(ValidationError):
        StockSplit(
            insId=1,
            splitDate="2020-01-01T00:00:00",
            splitRatio="not_a_float",
            splitType="forward",
        )

    # Invalid date format
    with pytest.raises(ValidationError):
        StockSplit(insId=1, splitDate="not_a_date", splitRatio=2.0, splitType="forward")

    # Valid data should not raise an error
    StockSplit(
        insId=1, splitDate="2020-01-01T00:00:00", splitRatio=2.0, splitType="forward"
    )

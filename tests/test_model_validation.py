"""Tests for model validation in the BorsdataClient."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.borsdata_client.models import (
    Branch, Instrument, StockPrice, KpiMetadata, Report, 
    InsiderRow, StockPriceLastValue, StockSplit
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
            listingDate="not_a_date"
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
        yahoo="TEST.ST"
    )


def test_stock_price_validation():
    """Test that StockPrice model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        StockPrice(d="2020-01-01")
    
    # Invalid type for h (high price)
    with pytest.raises(ValidationError):
        StockPrice(
            d="2020-01-01", 
            h="not_a_float", 
            l=90.0, 
            c=95.0, 
            o=92.0, 
            v=1000
        )
    
    # Valid data should not raise an error
    StockPrice(
        d="2020-01-01", 
        h=100.0, 
        l=90.0, 
        c=95.0, 
        o=92.0, 
        v=1000
    )


def test_kpi_metadata_validation():
    """Test that KpiMetadata model validates input data."""
    # Missing required field
    with pytest.raises(ValidationError):
        KpiMetadata(nameSv="Test KPI")
    
    # Invalid type for kpiId
    with pytest.raises(ValidationError):
        KpiMetadata(kpiId="not_an_int", nameSv="Test KPI", isString=False, format="percent")
    
    # Invalid type for isString
    with pytest.raises(ValidationError):
        KpiMetadata(kpiId=1, nameSv="Test KPI", isString="not_a_bool", format="percent")
    
    # Valid data should not raise an error
    KpiMetadata(kpiId=1, nameSv="Test KPI", isString=False, format="percent")


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
            non_Current_Assets=200.0
        )
    
    # Valid data should not raise an error
    Report(
        year=2020, 
        period=1, 
        revenues=1000.0,
        operating_Income=100.0, 
        profit_Before_Tax=80.0, 
        earnings_Per_Share=2.0, 
        number_Of_Shares=100.0, 
        dividend=1.0, 
        non_Current_Assets=200.0
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
            verificationDate="2020-01-01T00:00:00"
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
            verificationDate="not_a_date"
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
        verificationDate="2020-01-01T00:00:00"
    )


def test_stock_price_last_value_validation():
    """Test that StockPriceLastValue model validates input data."""
    # Missing required fields
    with pytest.raises(ValidationError):
        StockPriceLastValue(i=1)
    
    # Invalid type for i (instrument id)
    with pytest.raises(ValidationError):
        StockPriceLastValue(
            i="not_an_int", 
            d="2020-01-01", 
            h=100.0, 
            l=90.0, 
            c=95.0, 
            o=92.0, 
            v=1000
        )
    
    # Valid data should not raise an error
    StockPriceLastValue(
        i=1, 
        d="2020-01-01", 
        h=100.0, 
        l=90.0, 
        c=95.0, 
        o=92.0, 
        v=1000
    )


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
            splitType="forward"
        )
    
    # Invalid date format
    with pytest.raises(ValidationError):
        StockSplit(
            insId=1, 
            splitDate="not_a_date", 
            splitRatio=2.0, 
            splitType="forward"
        )
    
    # Valid data should not raise an error
    StockSplit(
        insId=1, 
        splitDate="2020-01-01T00:00:00", 
        splitRatio=2.0, 
        splitType="forward"
    ) 
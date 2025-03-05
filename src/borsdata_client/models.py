"""Pydantic models for the Borsdata API responses."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Branch(BaseModel):
    """Branch model representing a business branch/industry."""
    id: int = Field(description="Branch ID")
    name: Optional[str] = Field(None, description="Branch name")
    sector_id: int = Field(description="Branch sector ID", alias="sectorId")


class Country(BaseModel):
    """Country model."""
    id: int
    name: Optional[str]


class Market(BaseModel):
    """Market model."""
    id: int
    name: Optional[str]
    country_id: Optional[int] = Field(None, alias="countryId")
    is_index: Optional[bool] = Field(None, alias="isIndex")
    exchange_name: Optional[str] = Field(None, alias="exchangeName")


class Sector(BaseModel):
    """Sector model."""
    id: int
    name: Optional[str]


class Instrument(BaseModel):
    """Financial instrument model."""
    ins_id: int = Field(alias="insId")
    name: Optional[str]
    url_name: Optional[str] = Field(alias="urlName")
    instrument_type: int = Field(alias="instrument")
    isin: Optional[str]
    ticker: Optional[str]
    yahoo_symbol: Optional[str] = Field(alias="yahoo")
    sector_id: Optional[int] = Field(None, alias="sectorId")
    market_id: int = Field(alias="marketId")
    branch_id: Optional[int] = Field(None, alias="branchId")
    country_id: Optional[int] = Field(None, alias="countryId")
    listing_date: Optional[datetime] = Field(None, alias="listingDate")
    stock_price_currency: Optional[str] = Field(None, alias="stockPriceCurrency")
    report_currency: Optional[str] = Field(None, alias="reportCurrency")


class StockPrice(BaseModel):
    """Stock price data model."""
    d: str = Field(description="Date string in format YYYY-MM-DD")
    h: float = Field(description="High price")
    l: float = Field(description="Low price")
    c: float = Field(description="Closing price")
    o: float = Field(description="Opening price")
    v: int = Field(description="Volume")

    def get_date(self) -> datetime:
        """Convert the date string to a datetime object."""
        return datetime.strptime(self.d, "%Y-%m-%d")


class KpiMetadata(BaseModel):
    """KPI metadata model."""
    kpi_id: int = Field(alias="kpiId")
    name_sv: Optional[str] = Field(None, alias="nameSv")
    name_en: Optional[str] = Field(None, alias="nameEn")
    format: Optional[str]
    is_string: bool = Field(alias="isString")


class Report(BaseModel):
    """Financial report model."""
    year: int
    period: int
    revenues: Optional[float]
    gross_income: Optional[float] = Field(None, alias="gross_Income")
    operating_income: float = Field(alias="operating_Income")
    profit_before_tax: float = Field(alias="profit_Before_Tax")
    profit_to_equity_holders: Optional[float] = Field(None, alias="profit_To_Equity_Holders")
    earnings_per_share: float = Field(alias="earnings_Per_Share")
    number_of_shares: float = Field(alias="number_Of_Shares")
    dividend: float
    intangible_assets: Optional[float] = Field(None, alias="intangible_Assets")
    tangible_assets: Optional[float] = Field(None, alias="tangible_Assets")
    financial_assets: Optional[float] = Field(None, alias="financial_Assets")
    non_current_assets: float = Field(None, alias="non_Current_Assets")
    cash_and_equivalents: Optional[float] = Field(None, alias="cash_And_Equivalents")


# Response Models
class BranchesResponse(BaseModel):
    """Response model for branches endpoint."""
    branches: Optional[List[Branch]]


class CountriesResponse(BaseModel):
    """Response model for countries endpoint."""
    countries: Optional[List[Country]]


class MarketsResponse(BaseModel):
    """Response model for markets endpoint."""
    markets: Optional[List[Market]]


class InstrumentsResponse(BaseModel):
    """Response model for instruments endpoint."""
    instruments: Optional[List[Instrument]]


class StockPricesResponse(BaseModel):
    """Response model for stock prices endpoint."""
    instrument: int
    stockPricesList: List[Dict[str, Any]]  # The actual field name from the API 


class InsiderRow(BaseModel):
    """Model for insider trading data."""
    misc: bool
    owner_name: Optional[str] = Field(None, alias="ownerName")
    owner_position: Optional[str] = Field(None, alias="ownerPosition")
    equity_program: bool = Field(alias="equityProgram")
    shares: int
    price: float
    amount: float
    currency: Optional[str]
    transaction_type: int = Field(alias="transactionType")
    verification_date: datetime = Field(alias="verificationDate")
    transaction_date: Optional[datetime] = Field(None, alias="transactionDate")


class InsiderResponse(BaseModel):
    """Response model for insider holdings."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[InsiderRow]]
    error: Optional[str]


class InsiderListResponse(BaseModel):
    """Response model for list of insider holdings."""
    list: Optional[List[InsiderResponse]]


class ShortPosition(BaseModel):
    """Model for short position data."""
    position_holder: str = Field(alias="positionHolder")
    position: float
    date: datetime


class ShortsResponse(BaseModel):
    """Response model for short positions."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[ShortPosition]]
    error: Optional[str]


class ShortsListResponse(BaseModel):
    """Response model for list of short positions."""
    list: Optional[List[ShortsResponse]]


class BuybackRow(BaseModel):
    """Model for buyback data."""
    change: int
    change_proc: float = Field(alias="changeProc")
    price: float
    currency: Optional[str]
    shares: int
    shares_proc: float = Field(alias="sharesProc")
    date: datetime


class BuybackResponse(BaseModel):
    """Response model for buybacks."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[BuybackRow]]
    error: Optional[str]


class BuybackListResponse(BaseModel):
    """Response model for list of buybacks."""
    list: Optional[List[BuybackResponse]]


class InstrumentDescription(BaseModel):
    """Model for instrument description."""
    ins_id: int = Field(alias="insId")
    language_code: str = Field(alias="languageCode")
    text: Optional[str]
    error: Optional[str]


class InstrumentDescriptionListResponse(BaseModel):
    """Response model for list of instrument descriptions."""
    list: Optional[List[InstrumentDescription]]


class ReportCalendarDate(BaseModel):
    """Model for report calendar date."""
    release_date: datetime = Field(alias="releaseDate")
    report_type: Optional[str] = Field(None, alias="reportType")


class ReportCalendarResponse(BaseModel):
    """Response model for report calendar."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[ReportCalendarDate]]
    error: Optional[str]


class ReportCalendarListResponse(BaseModel):
    """Response model for list of report calendars."""
    list: Optional[List[ReportCalendarResponse]]


class DividendDate(BaseModel):
    """Model for dividend calendar date."""
    amount_paid: Optional[float] = Field(None, alias="amountPaid")
    currency_short_name: Optional[str] = Field(None, alias="currencyShortName")
    distribution_frequency: Optional[int] = Field(None, alias="distributionFrequency")
    excluding_date: Optional[datetime] = Field(None, alias="excludingDate")
    dividend_type: int = Field(alias="dividendType")


class DividendCalendarResponse(BaseModel):
    """Response model for dividend calendar."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[DividendDate]]
    error: Optional[str]


class DividendCalendarListResponse(BaseModel):
    """Response model for list of dividend calendars."""
    list: Optional[List[DividendCalendarResponse]]


class KpiValue(BaseModel):
    """Model for KPI value."""
    i: int = Field(description="Instrument Id")
    n: Optional[float] = Field(None, description="Numeric Value")
    s: Optional[str] = Field(None, description="String Value")


class KpiAllResponse(BaseModel):
    """Response model for all KPIs."""
    kpi_id: int = Field(alias="kpiId")
    group: Optional[str]
    calculation: Optional[str]
    values: Optional[List[KpiValue]]


class KpiCalcUpdatedResponse(BaseModel):
    """Response model for KPI calculation update time."""
    kpis_calc_updated: Optional[datetime] = Field(None, alias="kpisCalcUpdated")


class StockPriceLastValue(BaseModel):
    """Model for last stock price."""
    i: int = Field(description="Instrument Id")
    d: str = Field(description="Date string in format YYYY-MM-DD")
    h: float = Field(description="High price")
    l: float = Field(description="Low price")
    c: float = Field(description="Closing price")
    o: float = Field(description="Opening price")
    v: Optional[int] = Field(None, description="Volume")


class StockPriceLastResponse(BaseModel):
    """Response model for last stock prices."""
    stockPricesList: List[Dict[str, Any]]
    
    @property
    def values(self) -> List[StockPriceLastValue]:
        """Convert the stockPricesList to a list of StockPriceLastValue objects."""
        return [StockPriceLastValue(**item) for item in self.stockPricesList]


class StockSplit(BaseModel):
    """Model for stock split."""
    ins_id: int = Field(alias="insId")
    split_date: datetime = Field(alias="splitDate")
    split_ratio: float = Field(alias="splitRatio")
    split_type: str = Field(alias="splitType")


class StockSplitResponse(BaseModel):
    """Response model for stock splits."""
    stock_splits: List[StockSplit] = Field(alias="stockSplits")


class TranslationItem(BaseModel):
    """Model for translation item."""
    id: int
    name_sv: Optional[str] = Field(None, alias="nameSv")
    name_en: Optional[str] = Field(None, alias="nameEn")


class TranslationMetadataResponse(BaseModel):
    """Response model for translation metadata."""
    translationMetadatas: List[Dict[str, Any]]
    
    @property
    def branches(self) -> List[TranslationItem]:
        """Get branch translations."""
        result = []
        for item in self.translationMetadatas:
            if item.get("translationKey", "").startswith("L_BRANCH_"):
                try:
                    branch_id = int(item.get("translationKey", "").split("_")[-1])
                    result.append(TranslationItem(
                        id=branch_id,
                        nameSv=item.get("nameSv"),
                        nameEn=item.get("nameEn")
                    ))
                except (ValueError, IndexError):
                    pass
        return result
    
    @property
    def sectors(self) -> List[TranslationItem]:
        """Get sector translations."""
        result = []
        for item in self.translationMetadatas:
            if item.get("translationKey", "").startswith("L_SECTOR_"):
                try:
                    sector_id = int(item.get("translationKey", "").split("_")[-1])
                    result.append(TranslationItem(
                        id=sector_id,
                        nameSv=item.get("nameSv"),
                        nameEn=item.get("nameEn")
                    ))
                except (ValueError, IndexError):
                    pass
        return result
    
    @property
    def countries(self) -> List[TranslationItem]:
        """Get country translations."""
        result = []
        for item in self.translationMetadatas:
            if item.get("translationKey", "").startswith("L_COUNTRY_"):
                try:
                    country_id = int(item.get("translationKey", "").split("_")[-1])
                    result.append(TranslationItem(
                        id=country_id,
                        nameSv=item.get("nameSv"),
                        nameEn=item.get("nameEn")
                    ))
                except (ValueError, IndexError):
                    pass
        return result 
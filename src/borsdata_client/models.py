"""Pydantic models for the Borsdata API responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional

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
    """Single stock price entry."""

    d: Optional[str] = Field(None, description="Date string in format YYYY-MM-DD")
    h: Optional[float] = Field(None, description="Highest price")
    l: Optional[float] = Field(None, description="Lowest price")
    c: float = Field(..., description="Closing price")
    o: Optional[float] = Field(None, description="Opening price")
    v: Optional[int] = Field(None, description="Total volume")

    def get_date(self) -> Optional[datetime]:
        """Convert the date string to a datetime object."""
        if isinstance(self.d, str):
            return datetime.strptime(self.d, "%Y-%m-%d")
        return None


class KpiMetadata(BaseModel):
    """KPI metadata model."""

    kpi_id: int = Field(alias="kpiId")
    name_sv: Optional[str] = Field(None, alias="nameSv")
    name_en: Optional[str] = Field(None, alias="nameEn")
    format: Optional[str]
    is_string: bool = Field(alias="isString")


class KpiSummaryValue(BaseModel):
    year: int = Field(alias="y")
    period: int = Field(alias="p")
    value: Optional[float] = Field(None, alias="v")


class KpiSummaryGroup(BaseModel):
    kpi_id: int = Field(alias="KpiId")
    values: Optional[List[KpiSummaryValue]]


class KpisSummaryResponse(BaseModel):
    instrument: int
    report_type: Optional[str] = Field(None, alias="reportType")
    kpis: Optional[List[KpiSummaryGroup]]


class KpiHistory(BaseModel):
    y: int = Field(description="Year")
    p: int = Field(description="Period")
    v: Optional[float] = Field(None, description="Value (nullable)")

    @property
    def year(self) -> int:
        return self.y

    @property
    def period(self) -> int:
        return self.p

    @property
    def value(self) -> Optional[float]:
        return self.v


class KpisHistoryComp(BaseModel):
    instrument: int
    values: Optional[List[KpiHistory]] = Field(
        None, description="List of KPI history values"
    )
    error: Optional[str] = Field(None, description="Optional error message")
    kpi_id: Optional[int] = Field(None, alias="kpiId", description="KPI ID")

    # @property
    # def kpi_id(self) -> int:
    #     """ To comply with the other kpi-related models. """
    #     return self.instrument


class KpisHistoryArrayResp(BaseModel):
    kpi_id: int = Field(alias="kpiId")
    report_time: Optional[str] = Field(None, alias="reportTime")
    price_value: Optional[str] = Field(None, alias="priceValue")
    kpis_list: Optional[List[KpisHistoryComp]] = Field(None, alias="kpisList")


class Report(BaseModel):
    """Financial report model."""

    year: int
    period: int
    revenues: Optional[float]
    gross_income: Optional[float] = Field(None, alias="gross_Income")
    operating_income: float = Field(alias="operating_Income")
    profit_before_tax: float = Field(alias="profit_Before_Tax")
    profit_to_equity_holders: Optional[float] = Field(
        None, alias="profit_To_Equity_Holders"
    )
    earnings_per_share: float = Field(alias="earnings_Per_Share")
    number_of_shares: float = Field(alias="number_Of_Shares")
    dividend: float
    intangible_assets: Optional[float] = Field(None, alias="intangible_Assets")
    tangible_assets: Optional[float] = Field(None, alias="tangible_Assets")
    financial_assets: Optional[float] = Field(None, alias="financial_Assets")
    non_current_assets: float = Field(alias="non_Current_Assets")
    cash_and_equivalents: Optional[float] = Field(None, alias="cash_And_Equivalents")
    current_assets: float = Field(alias="current_Assets")
    total_assets: float = Field(alias="total_Assets")
    total_equity: float = Field(alias="total_Equity")
    non_current_liabilities: Optional[float] = Field(
        None, alias="non_Current_Liabilities"
    )
    current_liabilities: Optional[float] = Field(None, alias="current_Liabilities")
    total_liabilities_and_equity: float = Field(alias="total_Liabilities_And_Equity")
    net_debt: Optional[float] = Field(None, alias="net_Debt")
    cash_flow_from_operating_activities: Optional[float] = Field(
        None, alias="cash_Flow_From_Operating_Activities"
    )
    cash_flow_from_investing_activities: Optional[float] = Field(
        None, alias="cash_Flow_From_Investing_Activities"
    )
    cash_flow_from_financing_activities: Optional[float] = Field(
        None, alias="cash_Flow_From_Financing_Activities"
    )
    cash_flow_for_the_year: Optional[float] = Field(
        None, alias="cash_Flow_For_The_Year"
    )
    free_cash_flow: Optional[float] = Field(None, alias="free_Cash_Flow")
    stock_price_average: float = Field(alias="stock_Price_Average")
    stock_price_high: float = Field(alias="stock_Price_High")
    stock_price_low: float = Field(alias="stock_Price_Low")
    report_start_date: Optional[datetime] = Field(None, alias="report_Start_Date")
    report_end_date: Optional[datetime] = Field(None, alias="report_End_Date")
    broken_fiscal_year: Optional[bool] = Field(None, alias="broken_Fiscal_Year")
    currency: Optional[str] = Field(None, alias="currency")
    currency_ratio: Optional[float] = Field(None, alias="currency_Ratio")
    net_sales: Optional[float] = Field(None, alias="net_Sales")
    report_date: Optional[datetime] = Field(None, alias="report_Date")


class ReportsCombineResp(BaseModel):
    instrument: int
    error: Optional[str] = None
    reports_year: Optional[List[Report]] = Field(None, alias="reportsYear")
    reports_quarter: Optional[List[Report]] = Field(None, alias="reportsQuarter")
    reports_r12: Optional[List[Report]] = Field(None, alias="reportsR12")


class ReportsArrayResp(BaseModel):
    report_list: Optional[List[ReportsCombineResp]] = Field(None, alias="reportList")


class ReportMetadata(BaseModel):
    report_property: Optional[str] = Field(None, alias="reportPropery")
    name_sv: Optional[str] = Field(None, alias="nameSv")
    name_en: Optional[str] = Field(None, alias="nameEn")
    format: Optional[str] = None


class ReportMetadataResponse(BaseModel):
    report_metadatas: Optional[List[ReportMetadata]] = Field(
        None, alias="reportMetadatas"
    )


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


class SectorsResponse(BaseModel):
    """Response model for markets endpoint."""

    sectors: Optional[List[Sector]]


class InstrumentsResponse(BaseModel):
    """Response model for instruments endpoint."""

    instruments: Optional[List[Instrument]]


class StockPricesResponse(BaseModel):
    """Response model for stock prices endpoint."""

    instrument: int
    stockPricesList: List[Dict[str, Any]]  # The actual field name from the API


class StockPricesArrayRespList(BaseModel):
    """Stock prices list response for an instrument."""

    instrument: int = Field(..., description="Instrument ID")
    error: Optional[str] = Field(None, description="Error message, if any")
    stockPricesList: Optional[List[StockPrice]] = Field(
        None, description="List of stock prices"
    )


class StockPricesArrayResp(BaseModel):
    """Top-level response for stock prices array."""

    stockPricesArrayList: Optional[List[StockPricesArrayRespList]] = Field(
        None, description="List of stock prices per instrument"
    )


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
    error: Optional[str] = None


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
    error: Optional[str] = None


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
    error: Optional[str] = Field(None, alias="error")


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
    values: Optional[List[DividendDate]] = None
    error: Optional[str] = None


class DividendCalendarListResponse(BaseModel):
    """Response model for list of dividend calendars."""

    list: Optional[List[DividendCalendarResponse]] = None


class KpiValue(BaseModel):
    """Model for KPI value."""

    i: int = Field(description="Instrument Id")
    n: Optional[float] = Field(None, description="Numeric Value")
    s: Optional[str] = Field(None, description="String Value")


class KpiAllResponse(BaseModel):
    """Response model for all KPIs."""

    kpi_id: int = Field(alias="kpiId")
    group: Optional[str] = None
    calculation: Optional[str] = None
    values: Optional[List[KpiValue]] = None


class KpiCalcUpdatedResponse(BaseModel):
    """Response model for KPI calculation update time."""

    kpis_calc_updated: Optional[datetime] = Field(None, alias="kpisCalcUpdated")


class StockPriceLastValue(BaseModel):
    """Model for last stock price."""

    i: int = Field(description="Instrument Id")
    d: str = Field(description="Date string in format YYYY-MM-DD")
    o: float = Field(description="Opening price")
    h: float = Field(description="High price")
    l: float = Field(description="Low price")
    c: float = Field(description="Closing price")
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
                    result.append(
                        TranslationItem(
                            id=branch_id,
                            nameSv=item.get("nameSv"),
                            nameEn=item.get("nameEn"),
                        )
                    )
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
                    result.append(
                        TranslationItem(
                            id=sector_id,
                            nameSv=item.get("nameSv"),
                            nameEn=item.get("nameEn"),
                        )
                    )
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
                    result.append(
                        TranslationItem(
                            id=country_id,
                            nameSv=item.get("nameSv"),
                            nameEn=item.get("nameEn"),
                        )
                    )
                except (ValueError, IndexError):
                    pass
        return result

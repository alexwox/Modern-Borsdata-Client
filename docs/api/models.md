# Borsdata Models Reference

This document provides a comprehensive reference for the Pydantic models used in the BorsdataClient library.

## Core Models

### Branch

```python
class Branch(BaseModel):
    """Branch model representing a business branch/industry."""
    id: int = Field(description="Branch ID")
    name: Optional[str] = Field(None, description="Branch name")
    sector_id: int = Field(description="Branch sector ID", alias="sectorId")
```

### Country

```python
class Country(BaseModel):
    """Country model."""
    id: int
    name: Optional[str]
```

### Market

```python
class Market(BaseModel):
    """Market model."""
    id: int
    name: Optional[str]
    country_id: Optional[int] = Field(None, alias="countryId")
    is_index: Optional[bool] = Field(None, alias="isIndex")
    exchange_name: Optional[str] = Field(None, alias="exchangeName")
```

### Sector

```python
class Sector(BaseModel):
    """Sector model."""
    id: int
    name: Optional[str]
```

### Instrument

```python
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
```

### StockPrice

```python
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
```

### KpiMetadata

```python
class KpiMetadata(BaseModel):
    """KPI metadata model."""
    kpi_id: int = Field(alias="kpiId")
    name_sv: Optional[str] = Field(None, alias="nameSv")
    name_en: Optional[str] = Field(None, alias="nameEn")
    format: Optional[str]
    is_string: bool = Field(alias="isString")
```

### Report

```python
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
    # Note: This model has many more fields in the actual implementation
```

## Response Models

### BranchesResponse

```python
class BranchesResponse(BaseModel):
    """Response model for branches endpoint."""
    branches: Optional[List[Branch]]
```

### CountriesResponse

```python
class CountriesResponse(BaseModel):
    """Response model for countries endpoint."""
    countries: Optional[List[Country]]
```

### MarketsResponse

```python
class MarketsResponse(BaseModel):
    """Response model for markets endpoint."""
    markets: Optional[List[Market]]
```

### InstrumentsResponse

```python
class InstrumentsResponse(BaseModel):
    """Response model for instruments endpoint."""
    instruments: Optional[List[Instrument]]
```

### StockPricesResponse

```python
class StockPricesResponse(BaseModel):
    """Response model for stock prices endpoint."""
    instrument: int
    stockPricesList: List[Dict[str, Any]]  # The actual field name from the API
```

## Insider Trading Models

### InsiderRow

```python
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
```

### InsiderResponse

```python
class InsiderResponse(BaseModel):
    """Response model for insider holdings."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[InsiderRow]]
    error: Optional[str]
```

### InsiderListResponse

```python
class InsiderListResponse(BaseModel):
    """Response model for list of insider holdings."""
    list: Optional[List[InsiderResponse]]
```

## Short Position Models

### ShortPosition

```python
class ShortPosition(BaseModel):
    """Model for short position data."""
    position_holder: str = Field(alias="positionHolder")
    position: float
    date: datetime
```

### ShortsResponse

```python
class ShortsResponse(BaseModel):
    """Response model for short positions."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[ShortPosition]]
    error: Optional[str]
```

### ShortsListResponse

```python
class ShortsListResponse(BaseModel):
    """Response model for list of short positions."""
    list: Optional[List[ShortsResponse]]
```

## Buyback Models

### BuybackRow

```python
class BuybackRow(BaseModel):
    """Model for buyback data."""
    change: int
    change_proc: float = Field(alias="changeProc")
    price: float
    currency: Optional[str]
    shares: int
    shares_proc: float = Field(alias="sharesProc")
    date: datetime
```

### BuybackResponse

```python
class BuybackResponse(BaseModel):
    """Response model for buybacks."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[BuybackRow]]
    error: Optional[str]
```

### BuybackListResponse

```python
class BuybackListResponse(BaseModel):
    """Response model for list of buybacks."""
    list: Optional[List[BuybackResponse]]
```

## Instrument Description Models

### InstrumentDescription

```python
class InstrumentDescription(BaseModel):
    """Model for instrument description."""
    ins_id: int = Field(alias="insId")
    language_code: str = Field(alias="languageCode")
    text: Optional[str]
    error: Optional[str]
```

### InstrumentDescriptionListResponse

```python
class InstrumentDescriptionListResponse(BaseModel):
    """Response model for list of instrument descriptions."""
    list: Optional[List[InstrumentDescription]]
```

## Calendar Models

### ReportCalendarDate

```python
class ReportCalendarDate(BaseModel):
    """Model for report calendar date."""
    release_date: datetime = Field(alias="releaseDate")
    report_type: Optional[str] = Field(None, alias="reportType")
```

### ReportCalendarResponse

```python
class ReportCalendarResponse(BaseModel):
    """Response model for report calendar."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[ReportCalendarDate]]
    error: Optional[str]
```

### ReportCalendarListResponse

```python
class ReportCalendarListResponse(BaseModel):
    """Response model for list of report calendars."""
    list: Optional[List[ReportCalendarResponse]]
```

### DividendDate

```python
class DividendDate(BaseModel):
    """Model for dividend calendar date."""
    amount_paid: Optional[float] = Field(None, alias="amountPaid")
    currency_short_name: Optional[str] = Field(None, alias="currencyShortName")
    distribution_frequency: Optional[int] = Field(None, alias="distributionFrequency")
    excluding_date: Optional[datetime] = Field(None, alias="excludingDate")
    dividend_type: int = Field(alias="dividendType")
```

### DividendCalendarResponse

```python
class DividendCalendarResponse(BaseModel):
    """Response model for dividend calendar."""
    ins_id: int = Field(alias="insId")
    values: Optional[List[DividendDate]]
    error: Optional[str]
```

### DividendCalendarListResponse

```python
class DividendCalendarListResponse(BaseModel):
    """Response model for list of dividend calendars."""
    list: Optional[List[DividendCalendarResponse]]
```

## KPI Models

### KpiValue

```python
class KpiValue(BaseModel):
    """Model for KPI value."""
    i: int = Field(description="Instrument Id")
    n: Optional[float] = Field(None, description="Numeric Value")
    s: Optional[str] = Field(None, description="String Value")
```

### KpiAllResponse

```python
class KpiAllResponse(BaseModel):
    """Response model for all KPIs."""
    kpi_id: int = Field(alias="kpiId")
    group: Optional[str]
    calculation: Optional[str]
    values: Optional[List[KpiValue]]
```

### KpiCalcUpdatedResponse

```python
class KpiCalcUpdatedResponse(BaseModel):
    """Response model for KPI calculation update time."""
    kpis_calc_updated: Optional[datetime] = Field(None, alias="kpisCalcUpdated")
```

## Stock Price Models

### StockPriceLastValue

```python
class StockPriceLastValue(BaseModel):
    """Model for last stock price."""
    i: int = Field(description="Instrument Id")
    d: str = Field(description="Date string in format YYYY-MM-DD")
    h: float = Field(description="High price")
    l: float = Field(description="Low price")
    c: float = Field(description="Closing price")
    o: float = Field(description="Opening price")
    v: int = Field(description="Volume")
```

### StockPriceLastResponse

```python
class StockPriceLastResponse(BaseModel):
    """Response model for last stock prices."""
    values: List[StockPriceLastValue]
```

## Stock Split Models

### StockSplit

```python
class StockSplit(BaseModel):
    """Model for stock split."""
    ins_id: int = Field(alias="insId")
    split_date: datetime = Field(alias="splitDate")
    split_ratio: float = Field(alias="splitRatio")
    split_type: str = Field(alias="splitType")
```

### StockSplitResponse

```python
class StockSplitResponse(BaseModel):
    """Response model for stock splits."""
    stock_splits: List[StockSplit] = Field(alias="stockSplits")
```

## Translation Models

### TranslationItem

```python
class TranslationItem(BaseModel):
    """Model for translation item."""
    id: int
    name_sv: Optional[str] = Field(None, alias="nameSv")
    name_en: Optional[str] = Field(None, alias="nameEn")
```

### TranslationMetadataResponse

```python
class TranslationMetadataResponse(BaseModel):
    """Response model for translation metadata."""
    branches: Optional[List[TranslationItem]]
    sectors: Optional[List[TranslationItem]]
    countries: Optional[List[TranslationItem]]
```

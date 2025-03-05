"""Borsdata API client implementation."""

from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx
from .models import (
    BranchesResponse,
    CountriesResponse,
    MarketsResponse,
    InstrumentsResponse,
    StockPricesResponse,
    Branch,
    Country,
    Market,
    Instrument,
    StockPrice,
    Report,
    KpiMetadata,
    InsiderListResponse,
    ShortsListResponse,
    BuybackListResponse,
    InstrumentDescriptionListResponse,
    ReportCalendarListResponse,
    DividendCalendarListResponse,
    KpiAllResponse,
    KpiCalcUpdatedResponse,
    StockPriceLastResponse,
    StockPriceLastValue,
    StockSplit,
    StockSplitResponse,
    TranslationMetadataResponse,
)


class BorsdataClientError(Exception):
    """Base exception for Borsdata API client errors."""
    pass


class BorsdataClient:
    """Client for interacting with the Borsdata API."""

    BASE_URL = "https://apiservice.borsdata.se/v1"

    def __init__(self, api_key: str):
        """Initialize the Borsdata API client.
        
        Args:
            api_key: Your Borsdata API authentication key
        """
        self.api_key = api_key
        self._client = httpx.Client(timeout=30.0)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            BorsdataClientError: If the request fails
        """
        if params is None:
            params = {}
        params["authKey"] = self.api_key

        try:
            response = self._client.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()  # This will raise an HTTPError for 4XX/5XX responses
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = str(e)
            status_code = e.response.status_code
            raise BorsdataClientError(f"API request failed with status code {status_code}: {error_msg}") from e
        except Exception as e:
            raise BorsdataClientError(f"API request failed: {str(e)}") from e

    def get_branches(self) -> List[Branch]:
        """Get all branches/industries.
        
        Returns:
            List of Branch objects
        """
        response = self._get("/branches")
        return BranchesResponse(**response).branches or []

    def get_countries(self) -> List[Country]:
        """Get all countries.
        
        Returns:
            List of Country objects
        """
        response = self._get("/countries")
        return CountriesResponse(**response).countries or []

    def get_markets(self) -> List[Market]:
        """Get all markets.
        
        Returns:
            List of Market objects
        """
        response = self._get("/markets")
        return MarketsResponse(**response).markets or []

    def get_instruments(self) -> List[Instrument]:
        """Get all Nordic instruments.
        
        Returns:
            List of Instrument objects
        """
        response = self._get("/instruments")
        return InstrumentsResponse(**response).instruments or []

    def get_global_instruments(self) -> List[Instrument]:
        """Get all global instruments (requires Pro+ subscription).
        
        Returns:
            List of Instrument objects
        """
        response = self._get("/instruments/global")
        return InstrumentsResponse(**response).instruments or []

    def get_stock_prices(
        self,
        instrument_id: int,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        max_count: int = 20
    ) -> List[StockPrice]:
        """Get stock prices for an instrument.
        
        Args:
            instrument_id: ID of the instrument
            from_date: Start date for price data
            to_date: End date for price data
            max_count: Maximum number of price points to return
            
        Returns:
            List of StockPrice objects
        """
        params = {"maxCount": str(max_count)}
        
        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")

        response = self._get(f"/instruments/{instrument_id}/stockprices", params)
        response_model = StockPricesResponse(**response)
        
        # Convert each stock price dict to a StockPrice object
        return [StockPrice(**price) for price in response_model.stockPricesList]

    def get_reports(
        self,
        instrument_id: int,
        report_type: str = "year",
        max_count: int = 10,
        original_currency: bool = False
    ) -> List[Report]:
        """Get financial reports for an instrument.
        
        Args:
            instrument_id: ID of the instrument
            report_type: Type of report ('year', 'r12', or 'quarter')
            max_count: Maximum number of reports to return
            original_currency: Whether to return values in original currency
            
        Returns:
            List of Report objects
        """
        params = {
            "maxCount": str(max_count),
            "original": "1" if original_currency else "0"
        }
        
        response = self._get(f"/instruments/{instrument_id}/reports/{report_type}", params)
        return [Report(**report) for report in response.get("reports", [])]

    def get_kpi_metadata(self) -> List[KpiMetadata]:
        """Get metadata for all KPIs.
        
        Returns:
            List of KpiMetadata objects
        """
        response = self._get("/instruments/kpis/metadata")
        return [KpiMetadata(**kpi) for kpi in response.get("kpiHistoryMetadatas", [])]

    def get_insider_holdings(self, instrument_ids: List[int]) -> List[InsiderListResponse]:
        """Get insider holdings for specified instruments.
        
        Args:
            instrument_ids: List of instrument IDs to get insider holdings for
            
        Returns:
            List of insider holdings responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/holdings/insider", params)
        return InsiderListResponse(**response).list or []

    def get_short_positions(self) -> List[ShortsListResponse]:
        """Get short positions for all instruments.
        
        Returns:
            List of short positions responses
        """
        response = self._get("/holdings/shorts")
        return ShortsListResponse(**response).list or []

    def get_buybacks(self, instrument_ids: List[int]) -> List[BuybackListResponse]:
        """Get buyback data for specified instruments.
        
        Args:
            instrument_ids: List of instrument IDs to get buyback data for
            
        Returns:
            List of buyback responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/holdings/buyback", params)
        return BuybackListResponse(**response).list or []

    def get_instrument_descriptions(self, instrument_ids: List[int]) -> List[InstrumentDescriptionListResponse]:
        """Get descriptions for specified instruments.
        
        Args:
            instrument_ids: List of instrument IDs to get descriptions for
            
        Returns:
            List of instrument description responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/instruments/description", params)
        return InstrumentDescriptionListResponse(**response).list or []

    def get_report_calendar(self, instrument_ids: List[int]) -> List[ReportCalendarListResponse]:
        """Get report calendar for specified instruments.
        
        Args:
            instrument_ids: List of instrument IDs to get calendar for
            
        Returns:
            List of report calendar responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/instruments/report/calendar", params)
        return ReportCalendarListResponse(**response).list or []

    def get_dividend_calendar(self, instrument_ids: List[int]) -> List[DividendCalendarListResponse]:
        """Get dividend calendar for specified instruments.
        
        Args:
            instrument_ids: List of instrument IDs to get calendar for
            
        Returns:
            List of dividend calendar responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/instruments/dividend/calendar", params)
        return DividendCalendarListResponse(**response).list or []

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
            instrument_id: ID of the instrument
            kpi_id: ID of the KPI
            report_type: Type of report ('year', 'r12', 'quarter')
            price_type: Type of price calculation
            max_count: Maximum number of results to return
            
        Returns:
            List of KPI responses
        """
        params = {}
        if max_count:
            params["maxCount"] = str(max_count)
            
        response = self._get(
            f"/instruments/{instrument_id}/kpis/{kpi_id}/{report_type}/{price_type}/history",
            params
        )
        return KpiAllResponse(**response)

    def get_kpi_updated(self) -> datetime:
        """Get last update time for KPIs.
        
        Returns:
            Datetime of last KPI update
        """
        response = self._get("/instruments/kpis/updated")
        return KpiCalcUpdatedResponse(**response).kpis_calc_updated

    def get_last_stock_prices(self) -> List[StockPriceLastValue]:
        """Get last stock prices for all instruments.
        
        Returns:
            List of last stock prices
        """
        response = self._get("/instruments/stockprices/last")
        return StockPriceLastResponse(**response).values

    def get_last_global_stock_prices(self) -> List[StockPriceLastValue]:
        """Get last stock prices for all global instruments.
        
        Returns:
            List of last global stock prices
        """
        response = self._get("/instruments/stockprices/global/last")
        return StockPriceLastResponse(**response).values

    def get_stock_prices_by_date(self, date: datetime) -> List[StockPriceLastValue]:
        """Get stock prices for all instruments on a specific date.
        
        Args:
            date: Date to get prices for
            
        Returns:
            List of stock prices
        """
        params = {"date": date.strftime("%Y-%m-%d")}
        response = self._get("/instruments/stockprices/date", params)
        return StockPriceLastResponse(**response).values

    def get_global_stock_prices_by_date(self, date: datetime) -> List[StockPriceLastValue]:
        """Get stock prices for all global instruments on a specific date.
        
        Args:
            date: Date to get prices for
            
        Returns:
            List of global stock prices
        """
        params = {"date": date.strftime("%Y-%m-%d")}
        response = self._get("/instruments/stockprices/global/date", params)
        return StockPriceLastResponse(**response).values

    def get_stock_splits(self, from_date: Optional[datetime] = None) -> List[StockSplit]:
        """Get stock splits.
        
        Args:
            from_date: Optional start date to get splits from
            
        Returns:
            List of stock splits
        """
        params = {}
        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
            
        response = self._get("/instruments/StockSplits", params)
        return StockSplitResponse(**response).stock_splits

    def get_translation_metadata(self) -> TranslationMetadataResponse:
        """Get translation metadata.
        
        Returns:
            Translation metadata response
        """
        response = self._get("/translationmetadata")
        return TranslationMetadataResponse(**response)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._client.close() 
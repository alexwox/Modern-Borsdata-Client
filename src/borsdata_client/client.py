"""Borsdata API client implementation."""

from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import httpx
from tenacity import (
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

from .models import (
    Branch,
    BranchesResponse,
    BuybackListResponse,
    CountriesResponse,
    Country,
    DividendCalendarListResponse,
    InsiderListResponse,
    Instrument,
    InstrumentDescriptionListResponse,
    InstrumentsResponse,
    KpiAllResponse,
    KpiCalcUpdatedResponse,
    KpiMetadata,
    KpisHistoryArrayResp,
    KpisSummaryResponse,
    KpiSummaryGroup,
    Market,
    MarketsResponse,
    Report,
    ReportCalendarListResponse,
    ReportMetadata,
    ReportMetadataResponse,
    ReportsArrayResp,
    ReportsCombineResp,
    Sector,
    SectorsResponse,
    ShortsListResponse,
    StockPrice,
    StockPriceLastResponse,
    StockPriceLastValue,
    StockPricesArrayResp,
    StockPricesArrayRespList,
    StockPricesResponse,
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

    def __init__(self, api_key: str, retry: bool = True, max_retries: int = 5):
        """Initialize the Borsdata API client.

        Args:
            api_key: Your Borsdata API authentication key
            retry: Whether to enable retry on rate limit errors
            max_retries: Maximum number of retries for rate limit errors
        """
        self.api_key = api_key
        self._client = httpx.Client(timeout=30.0)
        self.retry = retry
        self.retryer = None

        def is_retryable_exception(exception):
            """Check if the exception is retryable."""
            if isinstance(exception, httpx.HTTPStatusError):
                # Retry for 429 Too Many Requests
                if exception.response.status_code == 429:
                    print("Rate limit exceeded. Retrying...")
                    return True
            return False

        self.retryer = Retrying(
            wait=wait_random_exponential(multiplier=1, min=1, max=20),
            stop=stop_after_attempt(max_retries),
            reraise=True,
            retry=retry_if_exception(is_retryable_exception),
        )

    def _get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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

        def _get_wrapper(api_endpoint=endpoint, params=params):
            response = self._client.get(api_endpoint, params=params)
            response.raise_for_status()  # This raises HTTPStatusError for 4xx/5xx codes
            return response.json()

        try:
            if self.retry:
                return self.retryer(
                    _get_wrapper,
                    api_endpoint=f"{self.BASE_URL}{endpoint}",
                    params=params,
                )
            else:
                return _get_wrapper(
                    api_endpoint=f"{self.BASE_URL}{endpoint}", params=params
                )

        except httpx.HTTPStatusError as e:
            error_msg = str(e)
            status_code = e.response.status_code
            raise BorsdataClientError(
                f"API request failed with status code {status_code}: {error_msg}"
            ) from e
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

    def get_sectors(self) -> List[Sector]:
        """Get all markets.

        Returns:
            List of Market objects
        """
        response = self._get("/sectors")
        return SectorsResponse(**response).sectors or []

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
        max_count: int = 20,
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

    def get_stock_prices_batch(
        self,
        instrument_ids: Iterable[int],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> List[StockPricesArrayRespList]:
        """Get stock prices for multiple instruments, max 50 instruments per call.

        Args:
            instrument_ids: Iterable of instrument IDs
            from_date: Start date for price data
            to_date: End date for price data

        Returns:
            List of StockPrice objects
        """
        assert isinstance(
            instrument_ids, Iterable
        ), "instrument_ids must be an iterable"
        assert (
            len(list(instrument_ids)) <= 50
        ), "Max 50 instrument IDs allowed per request"

        params = {"instList": ",".join(map(str, instrument_ids))}

        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")

        response = self._get("/instruments/stockprices", params)
        response_model = StockPricesArrayResp(**response)

        # Return list of instrument stock prices
        return response_model.stockPricesArrayList

    def get_reports(
        self,
        instrument_id: int,
        report_type: str = "year",
        max_count: int = 10,
        original_currency: bool = False,
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
            "original": "1" if original_currency else "0",
        }

        response = self._get(
            f"/instruments/{instrument_id}/reports/{report_type}", params
        )
        return [Report(**report) for report in response.get("reports", [])]

    def get_reports_batch(
        self,
        instrument_ids: Iterable[int],
        max_year_count: Optional[int] = 10,
        max_quarter_r12_count: Optional[int] = 10,
        original_currency: bool = False,
    ) -> List[ReportsCombineResp]:
        """Get financial reports for multiple instruments, max 50 instruments per call.

        Args:
            instrument_ids: Iterable of instrument IDs
            max_year_count: Maximum number of year reports to return, max 20.
            max_quarter_r12_count: Maximum number of quarter/R12 reports to return, max 40.
            original_currency: Whether to return values in original currency

        Returns:
            List of Report objects
        """
        assert isinstance(
            instrument_ids, Iterable
        ), "instrument_ids must be an iterable"
        assert (
            len(list(instrument_ids)) <= 50
        ), "Max 50 instrument IDs allowed per request"
        assert max_quarter_r12_count is None or isinstance(
            max_quarter_r12_count, int
        ), "max_quarter_r12_count must be an integer"
        assert max_year_count <= 20, "max_year_count must be 20 or less"
        assert max_quarter_r12_count <= 40, "max_quarter_r12_count must be 40 or less"

        params = {"instList": ",".join(map(str, instrument_ids))}

        if max_year_count is not None:
            assert (
                isinstance(max_year_count, int) and 0 < max_year_count <= 20
            ), "max_year_count must be a positive integer"
            params["maxYearCount"] = str(max_year_count)
        if max_quarter_r12_count is not None:
            assert (
                isinstance(max_quarter_r12_count, int)
                and 0 < max_quarter_r12_count <= 40
            ), "max_quarter_r12_count must be a positive integer"
            params["maxQuarterR12Count"] = str(max_quarter_r12_count)

        params["original"] = "1" if original_currency else "0"

        response = self._get(f"/instruments/reports", params)
        response_model = ReportsArrayResp(**response)
        return response_model.report_list

    def get_reports_metadata(
        self,
    ) -> List[ReportMetadata]:
        """Get financial reports metadata.

        Args:

        Returns:
            List of Report objects
        """

        response = self._get("/instruments/reports/metadata")
        response_model = ReportMetadataResponse(**response)
        return response_model.report_metadatas

    def get_kpi_metadata(self) -> List[KpiMetadata]:
        """Get metadata for all KPIs.

        Returns:
            List of KpiMetadata objects
        """
        response = self._get("/instruments/kpis/metadata")
        return [KpiMetadata(**kpi) for kpi in response.get("kpiHistoryMetadatas", [])]

    def get_kpi_updated(self) -> datetime:
        """Get last update time for KPIs.

        Returns:
            Datetime of last KPI update
        """
        response = self._get("/instruments/kpis/updated")
        return KpiCalcUpdatedResponse(**response).kpis_calc_updated

    def get_kpi_history(
        self,
        instrument_id: str,
        kpi_id: int,
        report_type: str,
        price_type: str = "mean",
        max_count: Optional[int] = None,
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
            params,
        )
        return KpiAllResponse(**response)

    def get_kpi_history_batch(
        self,
        instrument_ids: Iterable[int],
        kpi_id: int,
        report_type: str,
        price_type: str = "mean",
        max_count: Optional[int] = None,
    ) -> List[KpiAllResponse]:
        """Get KPI history for multiple instruments, max 50 instruments per call.

        Args:
            instrument_ids: IDs of the instruments
            kpi_id: ID of the KPI
            report_type: Type of report ('year', 'r12', 'quarter')
            price_type: Type of price calculation
            max_count: Maximum number of results to return, 10 by default. report_type 'year' can return max 20, 'r12' and 'quarter' can return max 40.

        Returns:
            List of KPI responses
        """

        assert isinstance(
            instrument_ids, Iterable
        ), "instrument_ids must be an iterable"
        assert (
            len(list(instrument_ids)) <= 50
        ), "Max 50 instrument IDs allowed per request"

        params = {"instList": ",".join(map(str, instrument_ids))}
        if max_count:
            params["maxCount"] = str(max_count)

        response = self._get(
            f"/instruments/kpis/{kpi_id}/{report_type}/{price_type}/history",
            params,
        )

        return KpisHistoryArrayResp(**response)

    def get_kpi_summary(
        self, instrument_id: int, report_type: str, max_count: Optional[int] = None
    ) -> List[KpiSummaryGroup]:
        """Get all KPI history for an instrument.

        Args:
            instrument_id: ID of the instrument
            report_type: Type of report ('year', 'r12', 'quarter')
            max_count: Maximum number of results to return

        Returns:
            List of all KPI responses
        """
        params = {}
        if max_count:
            params["maxCount"] = str(max_count)

        response = self._get(
            f"/instruments/{instrument_id}/kpis/{report_type}/summary", params
        )
        return KpisSummaryResponse(**response).kpis or []

    def get_insider_holdings(
        self, instrument_ids: Iterable[int]
    ) -> List[InsiderListResponse]:
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

    def get_buybacks(self, instrument_ids: Iterable[int]) -> List[BuybackListResponse]:
        """Get buyback data for specified instruments.

        Args:
            instrument_ids: List of instrument IDs to get buyback data for

        Returns:
            List of buyback responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/holdings/buyback", params)
        return BuybackListResponse(**response).list or []

    def get_instrument_descriptions(
        self, instrument_ids: Iterable[int]
    ) -> List[InstrumentDescriptionListResponse]:
        """Get descriptions for specified instruments.

        Args:
            instrument_ids: Iterable of instrument IDs to get descriptions for

        Returns:
            List of instrument description responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/instruments/description", params)
        return InstrumentDescriptionListResponse(**response).list or []

    def get_report_calendar(
        self, instrument_ids: Iterable[int]
    ) -> List[ReportCalendarListResponse]:
        """Get report calendar for specified instruments.

        Args:
            instrument_ids: Iterable of instrument IDs to get calendar for

        Returns:
            List of report calendar responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/instruments/report/calendar", params)
        return ReportCalendarListResponse(**response).list or []

    def get_dividend_calendar(
        self, instrument_ids: Iterable[int]
    ) -> List[DividendCalendarListResponse]:
        """Get dividend calendar for specified instruments.

        Args:
            instrument_ids: Iterable of instrument IDs to get calendar for

        Returns:
            List of dividend calendar responses
        """
        params = {"instList": ",".join(map(str, instrument_ids))}
        response = self._get("/instruments/dividend/calendar", params)
        return DividendCalendarListResponse(**response).list or []

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

    def get_global_stock_prices_by_date(
        self, date: datetime
    ) -> List[StockPriceLastValue]:
        """Get stock prices for all global instruments on a specific date.

        Args:
            date: Date to get prices for

        Returns:
            List of global stock prices
        """
        params = {"date": date.strftime("%Y-%m-%d")}
        response = self._get("/instruments/stockprices/global/date", params)
        return StockPriceLastResponse(**response).values

    def get_stock_splits(
        self, from_date: Optional[datetime] = None
    ) -> List[StockSplit]:
        """Get stock splits.

        Args:
            from_date: Optional start date to get splits from

        Returns:
            List of stock splits
        """
        params = {}
        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        response = self._get("/instruments/stocksplits", params)
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

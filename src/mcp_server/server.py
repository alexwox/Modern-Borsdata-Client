"""Borsdata MCP Server implementation.

This server provides tools for accessing Borsdata financial data through the MCP protocol.
Tools are organized into logical groups for efficient data access.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import Field

from borsdata_client import BorsdataClient


class BorsdataMCPServer:
    """MCP Server for Borsdata API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Borsdata MCP server.

        Args:
            api_key: Borsdata API key. If not provided, will look for BORSDATA_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("BORSDATA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Provide via constructor or BORSDATA_API_KEY env var."
            )

        self.server = Server("borsdata-server")
        self._client: Optional[BorsdataClient] = None
        self._register_tools()

    def _get_client(self) -> BorsdataClient:
        """Get or create the Borsdata client."""
        if self._client is None:
            self._client = BorsdataClient(self.api_key)
        return self._client

    def _register_tools(self) -> None:
        """Register all MCP tools."""
        # Reference Data Tools
        self.server.list_tools()(self._list_tools_handler)
        self.server.call_tool()(self._call_tool_handler)

    async def _list_tools_handler(self) -> List[Tool]:
        """List all available tools."""
        return [
            # Reference Data Tools
            Tool(
                name="get_instruments",
                description="Get all Nordic instruments (stocks). Returns a list of instruments with details like name, ISIN, ticker, market, sector, and industry information. Use this to find specific stocks or get an overview of available instruments.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_global_instruments",
                description="Get all global instruments (requires Pro+ subscription). Returns a list of global instruments with the same details as Nordic instruments.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_markets",
                description="Get all markets/exchanges. Returns a list of markets where instruments are traded (e.g., Stockholm Stock Exchange, Oslo Stock Exchange).",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_branches",
                description="Get all branches/industries. Returns a list of industry classifications that instruments belong to.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_sectors",
                description="Get all sectors. Returns a list of sector classifications that instruments belong to (e.g., Technology, Healthcare, Finance).",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_countries",
                description="Get all countries. Returns a list of countries where instruments are based.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            # Stock Price Tools
            Tool(
                name="get_stock_prices",
                description="Get historical stock prices for a single instrument. Returns daily price data including open, high, low, close, and volume. Use this for price analysis of a specific stock.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "integer",
                            "description": "The instrument ID (insId from get_instruments)",
                        },
                        "from_date": {
                            "type": "string",
                            "description": "Start date in YYYY-MM-DD format (optional)",
                        },
                        "to_date": {
                            "type": "string",
                            "description": "End date in YYYY-MM-DD format (optional)",
                        },
                        "max_count": {
                            "type": "integer",
                            "description": "Maximum number of price points to return (default: 20)",
                            "default": 20,
                        },
                    },
                    "required": ["instrument_id"],
                },
            ),
            Tool(
                name="get_stock_prices_batch",
                description="Get historical stock prices for multiple instruments at once (max 50). More efficient than calling get_stock_prices multiple times. Returns price data for all requested instruments.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs (max 50)",
                        },
                        "from_date": {
                            "type": "string",
                            "description": "Start date in YYYY-MM-DD format (optional)",
                        },
                        "to_date": {
                            "type": "string",
                            "description": "End date in YYYY-MM-DD format (optional)",
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            Tool(
                name="get_last_stock_prices",
                description="Get the most recent stock price for all Nordic instruments. Useful for getting a snapshot of current market prices.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_last_global_stock_prices",
                description="Get the most recent stock price for all global instruments (requires Pro+ subscription).",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_stock_prices_by_date",
                description="Get stock prices for all Nordic instruments on a specific date. Useful for historical market snapshots.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format",
                        },
                    },
                    "required": ["date"],
                },
            ),
            Tool(
                name="get_global_stock_prices_by_date",
                description="Get stock prices for all global instruments on a specific date (requires Pro+ subscription).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format",
                        },
                    },
                    "required": ["date"],
                },
            ),
            # Financial Reports Tools
            Tool(
                name="get_reports",
                description="Get financial reports for a single instrument. Returns detailed financial statements including revenue, profit, assets, etc. Can get yearly, quarterly, or R12 (rolling 12 months) reports.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "integer",
                            "description": "The instrument ID",
                        },
                        "report_type": {
                            "type": "string",
                            "enum": ["year", "r12", "quarter"],
                            "description": "Type of report (default: year)",
                            "default": "year",
                        },
                        "max_count": {
                            "type": "integer",
                            "description": "Maximum number of reports to return (default: 10)",
                            "default": 10,
                        },
                        "original_currency": {
                            "type": "boolean",
                            "description": "Return values in original currency (default: false)",
                            "default": False,
                        },
                    },
                    "required": ["instrument_id"],
                },
            ),
            Tool(
                name="get_reports_batch",
                description="Get financial reports for multiple instruments at once (max 50). More efficient for analyzing multiple companies.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs (max 50)",
                        },
                        "max_year_count": {
                            "type": "integer",
                            "description": "Max yearly reports to return (max 20, default: 10)",
                            "default": 10,
                        },
                        "max_quarter_r12_count": {
                            "type": "integer",
                            "description": "Max quarterly/R12 reports to return (max 40, default: 10)",
                            "default": 10,
                        },
                        "original_currency": {
                            "type": "boolean",
                            "description": "Return values in original currency (default: false)",
                            "default": False,
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            Tool(
                name="get_reports_metadata",
                description="Get metadata about all available financial report fields. Useful for understanding what data is available in financial reports.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            # KPI Tools
            Tool(
                name="get_kpi_metadata",
                description="Get metadata for all available KPIs (Key Performance Indicators). Returns information about metrics like P/E ratio, ROE, debt ratios, etc. Use this to understand available financial metrics.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_kpi_updated",
                description="Get the last update time for KPI data. Useful for knowing when the KPI data was last refreshed.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_kpi_history",
                description="Get historical KPI values for a single instrument. Track how a specific financial metric has changed over time (e.g., P/E ratio history).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "integer",
                            "description": "The instrument ID",
                        },
                        "kpi_id": {
                            "type": "integer",
                            "description": "The KPI ID (from get_kpi_metadata)",
                        },
                        "report_type": {
                            "type": "string",
                            "enum": ["year", "r12", "quarter"],
                            "description": "Type of report period",
                        },
                        "price_type": {
                            "type": "string",
                            "description": "Price calculation type (default: mean)",
                            "default": "mean",
                        },
                        "max_count": {
                            "type": "integer",
                            "description": "Maximum number of data points (optional)",
                        },
                    },
                    "required": ["instrument_id", "kpi_id", "report_type"],
                },
            ),
            Tool(
                name="get_kpi_history_batch",
                description="Get historical KPI values for multiple instruments at once (max 50). Efficient for comparing a specific metric across multiple companies.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs (max 50)",
                        },
                        "kpi_id": {
                            "type": "integer",
                            "description": "The KPI ID (from get_kpi_metadata)",
                        },
                        "report_type": {
                            "type": "string",
                            "enum": ["year", "r12", "quarter"],
                            "description": "Type of report period",
                        },
                        "price_type": {
                            "type": "string",
                            "description": "Price calculation type (default: mean)",
                            "default": "mean",
                        },
                        "max_count": {
                            "type": "integer",
                            "description": "Max data points: year max 20, r12/quarter max 40 (default: 10)",
                        },
                    },
                    "required": ["instrument_ids", "kpi_id", "report_type"],
                },
            ),
            Tool(
                name="get_kpi_summary",
                description="Get a summary of multiple KPIs for a single instrument. Returns an overview of various financial metrics for one company.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "integer",
                            "description": "The instrument ID",
                        },
                        "report_type": {
                            "type": "string",
                            "enum": ["year", "r12", "quarter"],
                            "description": "Type of report period",
                        },
                        "max_count": {
                            "type": "integer",
                            "description": "Maximum number of periods (optional)",
                        },
                    },
                    "required": ["instrument_id", "report_type"],
                },
            ),
            # Holdings Tools
            Tool(
                name="get_insider_holdings",
                description="Get insider holdings data for specified instruments. Shows ownership by company insiders (executives, board members, etc.).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs",
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            Tool(
                name="get_short_positions",
                description="Get short positions for all instruments. Shows which stocks are being heavily shorted, indicating bearish sentiment.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="get_buybacks",
                description="Get stock buyback data for specified instruments. Shows company share repurchase programs.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs",
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            # Calendar & Info Tools
            Tool(
                name="get_instrument_descriptions",
                description="Get detailed text descriptions for specified instruments. Provides company background and business descriptions.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs",
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            Tool(
                name="get_report_calendar",
                description="Get upcoming financial report dates for specified instruments. Useful for knowing when companies will release earnings.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs",
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            Tool(
                name="get_dividend_calendar",
                description="Get upcoming dividend dates for specified instruments. Shows when dividends will be paid and ex-dividend dates.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "instrument_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of instrument IDs",
                        },
                    },
                    "required": ["instrument_ids"],
                },
            ),
            # Stock Split & Translation Tools
            Tool(
                name="get_stock_splits",
                description="Get stock split information. Shows when and how stocks have been split, important for adjusting historical prices.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "from_date": {
                            "type": "string",
                            "description": "Start date in YYYY-MM-DD format (optional)",
                        },
                    },
                },
            ),
            Tool(
                name="get_translation_metadata",
                description="Get translation metadata for multilingual support. Returns translations for various data fields.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    async def _call_tool_handler(
        self, name: str, arguments: Dict[str, Any]
    ) -> List[TextContent]:
        """Handle tool calls."""
        try:
            client = self._get_client()

            # Reference Data Tools
            if name == "get_instruments":
                result = client.get_instruments()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([inst.model_dump() for inst in result], default=str),
                    )
                ]

            elif name == "get_global_instruments":
                result = client.get_global_instruments()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([inst.model_dump() for inst in result], default=str),
                    )
                ]

            elif name == "get_markets":
                result = client.get_markets()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([m.model_dump() for m in result], default=str),
                    )
                ]

            elif name == "get_branches":
                result = client.get_branches()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([b.model_dump() for b in result], default=str),
                    )
                ]

            elif name == "get_sectors":
                result = client.get_sectors()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([s.model_dump() for s in result], default=str),
                    )
                ]

            elif name == "get_countries":
                result = client.get_countries()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([c.model_dump() for c in result], default=str),
                    )
                ]

            # Stock Price Tools
            elif name == "get_stock_prices":
                instrument_id = arguments["instrument_id"]
                from_date = (
                    datetime.strptime(arguments["from_date"], "%Y-%m-%d")
                    if "from_date" in arguments
                    else None
                )
                to_date = (
                    datetime.strptime(arguments["to_date"], "%Y-%m-%d")
                    if "to_date" in arguments
                    else None
                )
                max_count = arguments.get("max_count", 20)

                result = client.get_stock_prices(
                    instrument_id=instrument_id,
                    from_date=from_date,
                    to_date=to_date,
                    max_count=max_count,
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([p.model_dump() for p in result], default=str),
                    )
                ]

            elif name == "get_stock_prices_batch":
                instrument_ids = arguments["instrument_ids"]
                from_date = (
                    datetime.strptime(arguments["from_date"], "%Y-%m-%d")
                    if "from_date" in arguments
                    else None
                )
                to_date = (
                    datetime.strptime(arguments["to_date"], "%Y-%m-%d")
                    if "to_date" in arguments
                    else None
                )

                result = client.get_stock_prices_batch(
                    instrument_ids=instrument_ids,
                    from_date=from_date,
                    to_date=to_date,
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([p.model_dump() for p in result], default=str),
                    )
                ]

            elif name == "get_last_stock_prices":
                result = client.get_last_stock_prices()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([p.model_dump() for p in result], default=str),
                    )
                ]

            elif name == "get_last_global_stock_prices":
                result = client.get_last_global_stock_prices()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([p.model_dump() for p in result], default=str),
                    )
                ]

            elif name == "get_stock_prices_by_date":
                date = datetime.strptime(arguments["date"], "%Y-%m-%d")
                result = client.get_stock_prices_by_date(date=date)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([p.model_dump() for p in result], default=str),
                    )
                ]

            elif name == "get_global_stock_prices_by_date":
                date = datetime.strptime(arguments["date"], "%Y-%m-%d")
                result = client.get_global_stock_prices_by_date(date=date)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([p.model_dump() for p in result], default=str),
                    )
                ]

            # Financial Reports Tools
            elif name == "get_reports":
                result = client.get_reports(
                    instrument_id=arguments["instrument_id"],
                    report_type=arguments.get("report_type", "year"),
                    max_count=arguments.get("max_count", 10),
                    original_currency=arguments.get("original_currency", False),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([r.model_dump() for r in result], default=str),
                    )
                ]

            elif name == "get_reports_batch":
                result = client.get_reports_batch(
                    instrument_ids=arguments["instrument_ids"],
                    max_year_count=arguments.get("max_year_count", 10),
                    max_quarter_r12_count=arguments.get("max_quarter_r12_count", 10),
                    original_currency=arguments.get("original_currency", False),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([r.model_dump() for r in result], default=str),
                    )
                ]

            elif name == "get_reports_metadata":
                result = client.get_reports_metadata()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([r.model_dump() for r in result], default=str),
                    )
                ]

            # KPI Tools
            elif name == "get_kpi_metadata":
                result = client.get_kpi_metadata()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([k.model_dump() for k in result], default=str),
                    )
                ]

            elif name == "get_kpi_updated":
                result = client.get_kpi_updated()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"kpis_calc_updated": result.isoformat()}),
                    )
                ]

            elif name == "get_kpi_history":
                result = client.get_kpi_history(
                    instrument_id=str(arguments["instrument_id"]),
                    kpi_id=arguments["kpi_id"],
                    report_type=arguments["report_type"],
                    price_type=arguments.get("price_type", "mean"),
                    max_count=arguments.get("max_count"),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result.model_dump(), default=str),
                    )
                ]

            elif name == "get_kpi_history_batch":
                result = client.get_kpi_history_batch(
                    instrument_ids=arguments["instrument_ids"],
                    kpi_id=arguments["kpi_id"],
                    report_type=arguments["report_type"],
                    price_type=arguments.get("price_type", "mean"),
                    max_count=arguments.get("max_count"),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result.model_dump(), default=str),
                    )
                ]

            elif name == "get_kpi_summary":
                result = client.get_kpi_summary(
                    instrument_id=arguments["instrument_id"],
                    report_type=arguments["report_type"],
                    max_count=arguments.get("max_count"),
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([k.model_dump() for k in result], default=str),
                    )
                ]

            # Holdings Tools
            elif name == "get_insider_holdings":
                result = client.get_insider_holdings(
                    instrument_ids=arguments["instrument_ids"]
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([h.model_dump() for h in result], default=str),
                    )
                ]

            elif name == "get_short_positions":
                result = client.get_short_positions()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([s.model_dump() for s in result], default=str),
                    )
                ]

            elif name == "get_buybacks":
                result = client.get_buybacks(instrument_ids=arguments["instrument_ids"])
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([b.model_dump() for b in result], default=str),
                    )
                ]

            # Calendar & Info Tools
            elif name == "get_instrument_descriptions":
                result = client.get_instrument_descriptions(
                    instrument_ids=arguments["instrument_ids"]
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([d.model_dump() for d in result], default=str),
                    )
                ]

            elif name == "get_report_calendar":
                result = client.get_report_calendar(
                    instrument_ids=arguments["instrument_ids"]
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([r.model_dump() for r in result], default=str),
                    )
                ]

            elif name == "get_dividend_calendar":
                result = client.get_dividend_calendar(
                    instrument_ids=arguments["instrument_ids"]
                )
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([d.model_dump() for d in result], default=str),
                    )
                ]

            # Stock Split & Translation Tools
            elif name == "get_stock_splits":
                from_date = (
                    datetime.strptime(arguments["from_date"], "%Y-%m-%d")
                    if "from_date" in arguments
                    else None
                )
                result = client.get_stock_splits(from_date=from_date)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps([s.model_dump() for s in result], default=str),
                    )
                ]

            elif name == "get_translation_metadata":
                result = client.get_translation_metadata()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result.model_dump(), default=str),
                    )
                ]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": str(e), "tool": name}),
                )
            ]

    async def run(self) -> None:
        """Run the MCP server."""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def main() -> None:
    """Main entry point for the server."""
    import asyncio

    server = BorsdataMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()


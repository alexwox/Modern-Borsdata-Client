# Borsdata MCP Server

An MCP (Model Context Protocol) server that exposes the Borsdata API through well-defined tools for AI agents.

## Overview

This MCP server provides AI assistants with structured access to Borsdata's financial data API. It includes 28 tools organized into logical categories for efficient data retrieval.

## Features

### Reference Data Tools

- **get_instruments** - Get all Nordic instruments (stocks)
- **get_global_instruments** - Get all global instruments (Pro+ required)
- **get_markets** - Get all markets/exchanges
- **get_branches** - Get all branches/industries
- **get_sectors** - Get all sectors
- **get_countries** - Get all countries

### Stock Price Tools

- **get_stock_prices** - Get historical prices for a single instrument
- **get_stock_prices_batch** - Get historical prices for multiple instruments (max 50)
- **get_last_stock_prices** - Get most recent prices for all Nordic instruments
- **get_last_global_stock_prices** - Get most recent prices for all global instruments
- **get_stock_prices_by_date** - Get prices for all instruments on a specific date
- **get_global_stock_prices_by_date** - Get global prices on a specific date

### Financial Reports Tools

- **get_reports** - Get financial reports for a single instrument
- **get_reports_batch** - Get financial reports for multiple instruments (max 50)
- **get_reports_metadata** - Get metadata about available financial report fields

### KPI (Key Performance Indicator) Tools

- **get_kpi_metadata** - Get metadata for all available KPIs
- **get_kpi_updated** - Get last KPI update timestamp
- **get_kpi_history** - Get historical KPI values for a single instrument
- **get_kpi_history_batch** - Get historical KPI values for multiple instruments
- **get_kpi_summary** - Get summary of multiple KPIs for an instrument

### Holdings Tools

- **get_insider_holdings** - Get insider holdings data
- **get_short_positions** - Get short positions for all instruments
- **get_buybacks** - Get stock buyback data

### Calendar & Info Tools

- **get_instrument_descriptions** - Get detailed company descriptions
- **get_report_calendar** - Get upcoming financial report dates
- **get_dividend_calendar** - Get upcoming dividend dates

### Other Tools

- **get_stock_splits** - Get stock split information
- **get_translation_metadata** - Get translation metadata for multilingual support

## Installation

### Prerequisites

1. Python 3.7 or higher
2. A valid Borsdata API key (get one from [Borsdata](https://borsdata.se))

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the main package with MCP support:

```bash
cd /path/to/Modern-Borsdata-Client
pip install -e .
pip install mcp>=1.0.0
```

## Configuration

### Environment Variables

Set your Borsdata API key as an environment variable:

```bash
export BORSDATA_API_KEY="your_api_key_here"
```

Or create a `.env` file in the project root:

```
BORSDATA_API_KEY=your_api_key_here
```

## Usage

### Running the Server

Run the MCP server directly:

```bash
python -m mcp_server.server
```

Or use the main entry point:

```bash
cd src/mcp_server
python server.py
```

### Using with Claude Desktop or Other MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop's config):

```json
{
  "mcpServers": {
    "borsdata": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "BORSDATA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Example Tool Usage

Once connected, AI assistants can use tools like:

```
Use get_instruments to list all available stocks.
Use get_stock_prices with instrument_id=123, from_date="2024-01-01", to_date="2024-12-31" to get historical prices.
Use get_reports with instrument_id=123, report_type="year" to get annual financial reports.
Use get_kpi_history with instrument_id=123, kpi_id=2, report_type="year" to track P/E ratio history.
```

## Tool Categories

### Efficient Data Retrieval

Tools are designed for efficient data access:

1. **Batch Tools** - When analyzing multiple stocks, use batch tools (e.g., `get_stock_prices_batch`, `get_reports_batch`) instead of calling single-instrument tools repeatedly. Batch tools support up to 50 instruments per call.

2. **Metadata Tools** - Use metadata tools first to understand available data:

   - `get_kpi_metadata` - See all available financial metrics
   - `get_reports_metadata` - See all available report fields
   - `get_instruments` - Get instrument IDs needed for other tools

3. **Date-specific Tools** - For market snapshots, use date-specific tools:
   - `get_stock_prices_by_date` - Get prices for all stocks on a specific date
   - `get_last_stock_prices` - Get most recent prices for all stocks

## API Rate Limits

The Borsdata API has rate limits (100 requests per 10 seconds). The client automatically:

- Retries on rate limit errors (429 status)
- Uses exponential backoff
- Supports up to 5 retries by default

## Data Format

All tools return JSON-formatted data with:

- Consistent field names (snake_case)
- ISO 8601 dates where applicable
- Type-validated responses using Pydantic models

## Error Handling

Errors are returned as JSON with:

```json
{
  "error": "Error message description",
  "tool": "tool_name_that_failed"
}
```

## Development

### Project Structure

```
mcp_server/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server implementation
├── requirements.txt     # MCP server dependencies
└── README.md           # This file
```

### Testing

The MCP server uses the same Borsdata client that's fully tested. See the main project's test suite:

```bash
cd /path/to/Modern-Borsdata-Client
pytest tests/
```

## Reference Links

- [Borsdata Official API Documentation](https://github.com/Borsdata-Sweden/API)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Main Borsdata Client Documentation](../../README.md)

## License

MIT License - See LICENSE file in the project root.

## Disclaimer

This is a third-party library and is not affiliated with Börsdata AB.

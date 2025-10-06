# Borsdata MCP Server - Usage Guide

This guide provides practical examples and tips for using the Borsdata MCP Server effectively.

## Quick Start

### 1. Install and Configure

```bash
# Install dependencies
pip install mcp>=1.0.0
cd /path/to/Modern-Borsdata-Client
pip install -e .

# Set your API key
export BORSDATA_API_KEY="your_api_key_here"
```

### 2. Run the Server

```bash
# From the project root
cd src
python -m mcp_server.server
```

### 3. Configure Your MCP Client

For Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "borsdata": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/Modern-Borsdata-Client/src",
      "env": {
        "BORSDATA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Common Usage Patterns

### Pattern 1: Finding and Analyzing a Stock

```
1. Get all instruments to find a stock:
   Tool: get_instruments

2. Find the instrument ID for "Volvo" or search through the results

3. Get stock prices for that instrument:
   Tool: get_stock_prices
   Args: {
     "instrument_id": 123,
     "from_date": "2024-01-01",
     "to_date": "2024-12-31",
     "max_count": 365
   }

4. Get financial reports:
   Tool: get_reports
   Args: {
     "instrument_id": 123,
     "report_type": "year",
     "max_count": 5
   }
```

### Pattern 2: Comparing Multiple Stocks

```
1. Get instruments and identify companies to compare

2. Get stock prices for all at once (much more efficient):
   Tool: get_stock_prices_batch
   Args: {
     "instrument_ids": [123, 456, 789],
     "from_date": "2024-01-01",
     "to_date": "2024-12-31"
   }

3. Get financial reports for all:
   Tool: get_reports_batch
   Args: {
     "instrument_ids": [123, 456, 789],
     "max_year_count": 5
   }

4. Compare a specific KPI across companies:
   Tool: get_kpi_history_batch
   Args: {
     "instrument_ids": [123, 456, 789],
     "kpi_id": 2,  # P/E ratio
     "report_type": "year"
   }
```

### Pattern 3: Market Overview

```
1. Get market structure:
   Tools: get_markets, get_sectors, get_branches

2. Get latest prices for all stocks:
   Tool: get_last_stock_prices

3. Find stocks with short positions:
   Tool: get_short_positions

4. Analyze by sector or market
```

### Pattern 4: Financial Analysis

```
1. Get KPI metadata to see available metrics:
   Tool: get_kpi_metadata

2. Get comprehensive KPI summary for a stock:
   Tool: get_kpi_summary
   Args: {
     "instrument_id": 123,
     "report_type": "year",
     "max_count": 5
   }

3. Track specific metrics over time:
   Tool: get_kpi_history
   Args: {
     "instrument_id": 123,
     "kpi_id": 2,  # Specific KPI
     "report_type": "year",
     "max_count": 10
   }
```

### Pattern 5: Event Tracking

```
1. Get upcoming earnings dates:
   Tool: get_report_calendar
   Args: {
     "instrument_ids": [123, 456, 789]
   }

2. Get upcoming dividend dates:
   Tool: get_dividend_calendar
   Args: {
     "instrument_ids": [123, 456, 789]
   }

3. Check insider activity:
   Tool: get_insider_holdings
   Args: {
     "instrument_ids": [123, 456, 789]
   }
```

## Tool Reference by Use Case

### Discovery & Search

- **get_instruments** - Find stocks by browsing all available
- **get_markets** - Filter by exchange
- **get_sectors** - Filter by sector
- **get_branches** - Filter by industry

### Price Analysis

- **get_stock_prices** - Historical prices for detailed analysis
- **get_stock_prices_batch** - Compare price movements
- **get_last_stock_prices** - Current market snapshot
- **get_stock_prices_by_date** - Historical market snapshot

### Fundamental Analysis

- **get_reports** - Financial statements
- **get_reports_metadata** - Understand available financial data
- **get_kpi_metadata** - See available metrics
- **get_kpi_history** - Track metric trends
- **get_kpi_summary** - Comprehensive financial overview

### Company Research

- **get_instrument_descriptions** - Company background
- **get_insider_holdings** - Insider ownership
- **get_buybacks** - Share repurchase programs
- **get_short_positions** - Short interest

### Event Planning

- **get_report_calendar** - Earnings dates
- **get_dividend_calendar** - Dividend dates
- **get_stock_splits** - Corporate actions

## Best Practices

### 1. Use Batch Tools for Efficiency

❌ **Inefficient:**

```
for instrument_id in [1, 2, 3, 4, 5]:
    get_stock_prices(instrument_id)
```

✅ **Efficient:**

```
get_stock_prices_batch([1, 2, 3, 4, 5])
```

### 2. Get Metadata First

When working with KPIs or reports, always check metadata first:

```
1. get_kpi_metadata() to see available metrics and their IDs
2. get_kpi_history() with the correct KPI ID
```

### 3. Use Appropriate Date Ranges

```python
# For recent data
"from_date": "2024-01-01"

# For long-term trends
"from_date": "2019-01-01"

# Limit data points
"max_count": 100
```

### 4. Handle Global vs Nordic Instruments

- Most tools work with Nordic instruments by default
- Global instruments require Pro+ subscription
- Use `get_global_instruments` and `get_last_global_stock_prices` for global markets

### 5. Understand Report Types

- **year** - Annual reports (most common)
- **quarter** - Quarterly reports
- **r12** - Rolling 12 months (trailing twelve months)

Choose based on your analysis needs:

- Long-term trends → `year`
- Recent performance → `quarter`
- Current annualized metrics → `r12`

## Data Fields Reference

### Instrument Object

```json
{
  "ins_id": 123, // Instrument ID (use this for other calls)
  "name": "Volvo", // Company name
  "ticker": "VOLV-B", // Stock ticker
  "isin": "SE0000115446", // ISIN code
  "market_id": 1, // Market/exchange ID
  "sector_id": 5, // Sector ID
  "branch_id": 45 // Industry ID
}
```

### Stock Price Object

```json
{
  "d": "2024-01-15", // Date
  "c": 123.45, // Close price
  "h": 125.0, // High price
  "l": 122.0, // Low price
  "o": 123.0, // Open price
  "v": 1000000 // Volume
}
```

### Report Object (simplified)

```json
{
  "year": 2023,
  "period": "Q4",
  "revenues": 50000000,
  "gross_profit": 15000000,
  "operating_profit": 10000000,
  "net_income": 8000000
  // ... many more fields
}
```

## Troubleshooting

### Error: "No module named 'mcp'"

```bash
pip install mcp>=1.0.0
```

### Error: "API key required"

```bash
export BORSDATA_API_KEY="your_key_here"
```

### Error: "Rate limit exceeded"

The client automatically retries. If you see this error:

- Wait a few seconds
- Reduce the number of calls
- Use batch tools instead of individual calls

### Error: "Requires Pro+ subscription"

Some features require a Pro+ subscription:

- Global instruments
- Extended historical data
- Real-time updates

## Example: Complete Analysis Workflow

```
# 1. Find companies in tech sector
get_sectors() → find "Technology" sector_id = 5
get_instruments() → filter by sector_id = 5

# 2. Get prices for top 10 tech companies
get_stock_prices_batch({
  "instrument_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "from_date": "2023-01-01",
  "to_date": "2024-12-31"
})

# 3. Get financial reports
get_reports_batch({
  "instrument_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "max_year_count": 3
})

# 4. Compare P/E ratios
get_kpi_metadata() → find P/E ratio KPI ID
get_kpi_history_batch({
  "instrument_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "kpi_id": 2,
  "report_type": "year",
  "max_count": 5
})

# 5. Check for upcoming events
get_report_calendar({"instrument_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
get_dividend_calendar({"instrument_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
```

## Support

For issues or questions:

- Check the main [README](README.md)
- Review the [Borsdata Client Documentation](../../README.md)
- See [Borsdata Official API Docs](https://github.com/Borsdata-Sweden/API)

## Tips for AI Assistants

When helping users with this MCP server:

1. **Start broad, then narrow**: Get instruments → filter → analyze specific ones
2. **Use batch tools**: Always prefer batch operations for multiple instruments
3. **Check metadata**: Reference KPI/report metadata before requesting specific data
4. **Be date-aware**: Consider appropriate time ranges for the analysis
5. **Handle errors gracefully**: Rate limits are normal, the client handles retries
6. **Explain results**: Present data in user-friendly formats with context

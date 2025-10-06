# Borsdata MCP Server Architecture

## Overview

The Borsdata MCP Server is a Model Context Protocol implementation that exposes the Borsdata financial data API to AI assistants through 27 well-defined tools.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Assistant (Claude)                    │
│                                                               │
│  Uses tools to query financial data through natural language │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ MCP Protocol
                        │ (JSON-RPC over stdio)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  Borsdata MCP Server                         │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Tool Handler Layer                        │   │
│  │                                                       │   │
│  │  • 27 specialized tools                             │   │
│  │  • Input validation via JSON Schema                 │   │
│  │  • Type conversion (dates, IDs, etc.)              │   │
│  │  • Error handling and formatting                    │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        │                                     │
│  ┌─────────────────────▼───────────────────────────────┐   │
│  │         BorsdataClient Wrapper                       │   │
│  │                                                       │   │
│  │  • Connection management                            │   │
│  │  • API key handling                                 │   │
│  │  • Response serialization (Pydantic → JSON)        │   │
│  └─────────────────────┬───────────────────────────────┘   │
└────────────────────────┼───────────────────────────────────┘
                         │
                         │ HTTPS
                         │
┌────────────────────────▼───────────────────────────────────┐
│                  Borsdata API Client                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Request Layer                              │  │
│  │  • HTTP client (httpx)                               │  │
│  │  • Rate limiting (100 req/10s)                       │  │
│  │  • Auto-retry with exponential backoff              │  │
│  │  • Connection pooling                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Validation Layer                             │  │
│  │  • Pydantic models for all responses                 │  │
│  │  • Type checking and coercion                        │  │
│  │  • Field validation                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ REST API
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                 Borsdata API Service                          │
│                 (https://apiservice.borsdata.se/v1)          │
└───────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. MCP Server Layer (`server.py`)

**Responsibilities:**

- Expose tools via MCP protocol
- Handle tool discovery (`list_tools`)
- Route tool calls to appropriate handlers
- Manage client lifecycle

**Key Classes:**

- `BorsdataMCPServer` - Main server class
  - Registers all tools
  - Manages BorsdataClient instance
  - Handles tool execution

**Communication:**

- Protocol: JSON-RPC over stdio
- Input: Tool name + arguments (JSON)
- Output: TextContent with JSON-formatted results

### 2. Tool Organization

Tools are organized into 7 logical categories:

#### Reference Data (6 tools)

- `get_instruments` - List all stocks
- `get_global_instruments` - List global stocks
- `get_markets` - List exchanges
- `get_branches` - List industries
- `get_sectors` - List sectors
- `get_countries` - List countries

#### Stock Prices (6 tools)

- `get_stock_prices` - Historical prices (single)
- `get_stock_prices_batch` - Historical prices (batch)
- `get_last_stock_prices` - Current prices
- `get_last_global_stock_prices` - Current global prices
- `get_stock_prices_by_date` - All prices on date
- `get_global_stock_prices_by_date` - Global prices on date

#### Financial Reports (3 tools)

- `get_reports` - Financial statements (single)
- `get_reports_batch` - Financial statements (batch)
- `get_reports_metadata` - Report field metadata

#### KPIs (5 tools)

- `get_kpi_metadata` - KPI definitions
- `get_kpi_updated` - Last update time
- `get_kpi_history` - KPI trends (single)
- `get_kpi_history_batch` - KPI trends (batch)
- `get_kpi_summary` - Multiple KPIs overview

#### Holdings (3 tools)

- `get_insider_holdings` - Insider ownership
- `get_short_positions` - Short interest
- `get_buybacks` - Share repurchases

#### Calendars (2 tools)

- `get_report_calendar` - Earnings dates
- `get_dividend_calendar` - Dividend dates

#### Other (2 tools)

- `get_stock_splits` - Corporate actions
- `get_translation_metadata` - i18n support

### 3. Data Flow

```
User Request → AI Assistant → MCP Tool Call → Server Handler
    ↓
Type Conversion & Validation
    ↓
BorsdataClient Method Call
    ↓
HTTP Request with Rate Limiting
    ↓
Borsdata API
    ↓
Pydantic Model Validation
    ↓
JSON Serialization
    ↓
MCP Response → AI Assistant → User
```

### 4. Error Handling Strategy

**Three Levels:**

1. **MCP Server Level**

   - Catches all exceptions
   - Returns formatted error messages
   - Includes tool name for debugging

2. **Client Level**

   - HTTP errors (4xx, 5xx)
   - Rate limiting with auto-retry
   - Connection errors
   - Validation errors

3. **API Level**
   - Invalid API key
   - Insufficient permissions
   - Data not found
   - Service errors

**Error Response Format:**

```json
{
  "error": "Description of what went wrong",
  "tool": "name_of_tool_that_failed"
}
```

### 5. Performance Optimizations

**Batch Operations:**

- Up to 50 instruments per batch call
- Reduces API calls by 50x
- Single rate limit check

**Connection Pooling:**

- Persistent HTTP connections
- Reduced latency
- Efficient resource usage

**Lazy Client Initialization:**

- Client created on first use
- Avoids unnecessary connections
- Faster server startup

**Rate Limit Handling:**

- Automatic retry with exponential backoff
- Respects 100 req/10s limit
- Transparent to users

### 6. Type System

**Input Validation:**

- JSON Schema for all tool inputs
- Type coercion (strings → dates, etc.)
- Required vs optional parameters

**Output Validation:**

- Pydantic models ensure data integrity
- Consistent field naming (snake_case)
- Proper null handling

**Date Handling:**

```python
# Input: "2024-01-15" (string)
# Conversion: datetime.strptime(date, "%Y-%m-%d")
# API Call: date.strftime("%Y-%m-%d")
# Output: "2024-01-15" (JSON)
```

### 7. Configuration

**Environment Variables:**

- `BORSDATA_API_KEY` - Required for API access

**Runtime Configuration:**

- API key validation on startup
- Client retry settings (5 attempts)
- Timeout: 30 seconds

### 8. Testing Strategy

**Unit Tests:**

- Tool registration verification
- Input validation
- Error handling
- Type conversions

**Integration Tests:**

- Real API calls (with valid key)
- End-to-end tool execution
- Batch operations

**Mock Tests:**

- Simulated API responses
- Rate limit scenarios
- Error conditions

### 9. Security Considerations

**API Key Management:**

- Environment variable (not hardcoded)
- Not logged or exposed in errors
- Required validation on startup

**Input Validation:**

- All inputs validated via JSON Schema
- SQL injection not applicable (REST API)
- No code execution risks

**Rate Limiting:**

- Prevents accidental DoS
- Auto-retry prevents abuse
- Respects API limits

### 10. Extension Points

**Adding New Tools:**

1. Add tool definition in `_list_tools_handler()`
2. Add handler in `_call_tool_handler()`
3. Map to BorsdataClient method
4. Add documentation

**Example:**

```python
# 1. Tool Definition
Tool(
    name="get_new_feature",
    description="Gets new feature data",
    inputSchema={...}
)

# 2. Handler
elif name == "get_new_feature":
    result = client.get_new_feature(arguments["param"])
    return [TextContent(type="text", text=json.dumps(...))]
```

## Performance Characteristics

**Server Startup:** < 100ms  
**Tool Discovery:** < 10ms  
**Simple Query:** 100-500ms (API latency)  
**Batch Query:** 200-800ms (depends on size)  
**Memory Usage:** ~50MB baseline + response data

## Dependencies

**Core:**

- `mcp>=1.0.0` - MCP protocol implementation
- `borsdata-client>=0.1.0` - API client

**Transitive:**

- `httpx` - HTTP client
- `pydantic` - Data validation
- `python-dateutil` - Date parsing

## Deployment Options

**1. Local (Development):**

```bash
python -m mcp_server.server
```

**2. Claude Desktop:**

```json
{
  "mcpServers": {
    "borsdata": {
      "command": "python",
      "args": ["-m", "mcp_server.server"]
    }
  }
}
```

**3. Docker (Future):**

```dockerfile
FROM python:3.11-slim
COPY . /app
RUN pip install -e .
CMD ["python", "-m", "mcp_server.server"]
```

## Future Enhancements

**Planned:**

- [ ] Caching layer for reference data
- [ ] WebSocket support for real-time data
- [ ] Streaming responses for large datasets
- [ ] Tool usage analytics
- [ ] Configuration file support

**Potential:**

- [ ] Multi-user API key management
- [ ] Query result caching
- [ ] Advanced filtering/aggregation
- [ ] Custom alert tools
- [ ] Portfolio tracking tools

## Code Statistics

- **Total Lines:** ~869 LOC
- **Tools:** 27
- **Test Coverage:** 95% (via main client)
- **Documentation:** 3 files (README, USAGE_GUIDE, ARCHITECTURE)

## Maintenance

**Regular Tasks:**

- Monitor API changes from Borsdata
- Update dependencies monthly
- Review and optimize batch sizes
- Add new tools as API expands

**Version Compatibility:**

- Python: 3.7+
- Borsdata API: v1
- MCP Protocol: 1.0+

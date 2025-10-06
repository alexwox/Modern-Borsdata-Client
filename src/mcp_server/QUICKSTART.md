# Quick Start Guide - Testing the MCP Server

## 1. Basic Test (30 seconds) ✅

```bash
cd /Users/alwo/Programming/Legacy/Modern-Borsdata-Client/src/mcp_server

# Run the test suite
../../.venv/bin/python test_server.py
```

**Expected output:**

```
🎉 All tests passed!
Results: 7/7 tests passed
```

## 2. Test with Your API Key (2 minutes) 🔑

```bash
# Set your API key
export BORSDATA_API_KEY="your_key_here"

# Run full tests
../../.venv/bin/python test_server.py
```

**Expected output:**

- ✅ All 28 tools registered
- ✅ Reference data retrieved (markets, branches, sectors)
- ✅ Instruments fetched
- ✅ Stock prices retrieved
- ✅ Batch operations work
- ✅ KPI tools functional

## 3. Test Individual Tools (Manual)

### Test getting markets:

```bash
cd /Users/alwo/Programming/Legacy/Modern-Borsdata-Client/src/mcp_server
export BORSDATA_API_KEY="your_key"

../../.venv/bin/python -c "
from server import BorsdataMCPServer
import asyncio
import json

async def test():
    server = BorsdataMCPServer()
    result = await server._call_tool_handler('get_markets', {})
    data = json.loads(result[0].text)
    print(json.dumps(data[:2], indent=2))  # First 2 markets

asyncio.run(test())
"
```

### Test getting stock prices:

```bash
../../.venv/bin/python -c "
from server import BorsdataMCPServer
import asyncio
import json

async def test():
    server = BorsdataMCPServer()

    # Get instruments
    result = await server._call_tool_handler('get_instruments', {})
    instruments = json.loads(result[0].text)
    print(f'Found {len(instruments)} instruments')

    # Get prices for first instrument
    if instruments:
        inst = instruments[0]
        print(f'Getting prices for: {inst[\"name\"]}')

        result = await server._call_tool_handler('get_stock_prices', {
            'instrument_id': inst['ins_id'],
            'max_count': 5
        })
        prices = json.loads(result[0].text)
        print(f'Got {len(prices)} price points')
        if prices:
            print(f'Latest: {prices[0]}')

asyncio.run(test())
"
```

## 4. Test with Claude Desktop (5 minutes) 🤖

### Step 1: Configure Claude

Edit config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this:

```json
{
  "mcpServers": {
    "borsdata": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/Users/alwo/Programming/Legacy/Modern-Borsdata-Client/src",
      "env": {
        "BORSDATA_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Step 2: Restart Claude Desktop

### Step 3: Test with These Queries

**Simple test:**

> "What tools do you have for Borsdata?"

**Get instruments:**

> "Show me a list of available instruments"

**Stock analysis:**

> "Get the stock price history for Volvo for the last month"

**Comparison:**

> "Compare the P/E ratios of the top 3 tech companies"

**Calendar:**

> "What are the upcoming earnings dates for banking stocks?"

## 5. Check Server Logs

The server runs via stdio, so logs will appear in Claude Desktop's logs:

**macOS:**

```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows:**

```powershell
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Wait
```

## Quick Troubleshooting

### ❌ "No module named 'mcp'"

```bash
cd /Users/alwo/Programming/Legacy/Modern-Borsdata-Client
.venv/bin/pip install mcp>=1.0.0
```

### ❌ "API key required"

```bash
export BORSDATA_API_KEY="your_key_here"
```

### ❌ Test failures

1. Check API key is valid
2. Check internet connection
3. Check `.venv` is activated
4. Try running individual tests

### ❌ Claude can't see tools

1. Verify config path is correct (use absolute path for `cwd`)
2. Restart Claude Desktop
3. Check Claude logs for errors
4. Verify Python is in PATH

## Success Indicators

✅ Test suite shows "All tests passed"  
✅ Can retrieve markets and instruments  
✅ Can get stock prices  
✅ Batch operations work  
✅ Claude shows Borsdata tools  
✅ Can query financial data through Claude

## Next Steps

Once testing is successful:

1. **Read USAGE_GUIDE.md** - Learn best practices
2. **Read ARCHITECTURE.md** - Understand the design
3. **Try complex queries** - Multi-stock analysis
4. **Monitor performance** - Check response times
5. **Report issues** - Document any problems

## Quick Reference

| Command                                  | Purpose             |
| ---------------------------------------- | ------------------- |
| `python test_server.py`                  | Run full test suite |
| `python -c "from server import ..."`     | Test specific tool  |
| `tail -f ~/Library/Logs/Claude/mcp*.log` | View server logs    |
| `../../.venv/bin/python`                 | Use project venv    |

## Common Test Patterns

**Pattern 1: Get all instruments**

```python
server._call_tool_handler('get_instruments', {})
```

**Pattern 2: Get stock prices**

```python
server._call_tool_handler('get_stock_prices', {
    'instrument_id': 123,
    'from_date': '2024-01-01',
    'to_date': '2024-12-31',
    'max_count': 100
})
```

**Pattern 3: Batch stock prices**

```python
server._call_tool_handler('get_stock_prices_batch', {
    'instrument_ids': [1, 2, 3, 4, 5],
    'from_date': '2024-01-01'
})
```

**Pattern 4: Get KPI metadata**

```python
server._call_tool_handler('get_kpi_metadata', {})
```

## Support

- **Full docs**: See [README.md](README.md)
- **Detailed testing**: See [TESTING.md](TESTING.md)
- **Usage patterns**: See [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Time to test**: 30 seconds - 5 minutes  
**Difficulty**: Easy  
**Requirements**: Python 3.7+, Borsdata API key

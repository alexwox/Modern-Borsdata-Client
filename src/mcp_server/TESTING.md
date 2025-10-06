# Testing the Borsdata MCP Server

This guide explains how to test the MCP server in various ways, from basic validation to full integration testing.

## Quick Test

The fastest way to verify the server is working:

```bash
cd /Users/alwo/Programming/Legacy/Modern-Borsdata-Client/src/mcp_server

# Test 1: Verify imports work
python -c "from server import BorsdataMCPServer; print('✅ Import successful')"

# Test 2: Run the automated test suite
python test_server.py
```

## Testing Methods

### 1. Automated Test Suite (Recommended)

The `test_server.py` script runs comprehensive tests:

```bash
# Without API key (structure tests only)
python test_server.py

# With API key (full tests)
export BORSDATA_API_KEY="your_key_here"
python test_server.py
```

**What it tests:**

- ✅ All 27 tools are registered
- ✅ Tool schemas are valid
- ✅ Reference data retrieval
- ✅ Stock price queries
- ✅ Batch operations
- ✅ KPI tools
- ✅ Error handling

### 2. Manual Testing with MCP Inspector

Use the MCP Inspector tool to interactively test the server:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run with your server
mcp-inspector python -m mcp_server.server
```

This opens a web interface where you can:

- See all available tools
- Test tool calls with custom parameters
- View responses in real-time

### 3. Testing with Claude Desktop

The ultimate test - use the server with Claude:

#### Step 1: Configure Claude Desktop

Edit your config file (location depends on OS):

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add:

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

#### Step 2: Restart Claude Desktop

#### Step 3: Test with Queries

Ask Claude things like:

- "Get me a list of all available instruments"
- "Show me the stock price history for Volvo for the last month"
- "Compare the P/E ratios of the top 5 tech companies"
- "What are the upcoming earnings dates for banking stocks?"

### 4. Unit Testing Individual Tools

Test specific tools programmatically:

```python
import asyncio
import os
from mcp_server.server import BorsdataMCPServer

async def test_specific_tool():
    api_key = os.environ.get("BORSDATA_API_KEY")
    server = BorsdataMCPServer(api_key)

    # Test get_markets
    result = await server._call_tool_handler("get_markets", {})
    print(result[0].text)

    # Test get_stock_prices
    result = await server._call_tool_handler("get_stock_prices", {
        "instrument_id": 3,
        "max_count": 5
    })
    print(result[0].text)

asyncio.run(test_specific_tool())
```

### 5. Testing Without API Key

You can test the structure without a valid API key:

```bash
# This tests tool registration and schemas
python test_server.py
```

The tests will skip API calls but verify:

- All tools are properly registered
- Schemas are valid
- Error handling works

## Common Test Scenarios

### Test 1: Basic Connectivity

```bash
# Test that server starts
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio

async def test():
    server = BorsdataMCPServer('test_key')
    tools = await server._list_tools_handler()
    print(f'Found {len(tools)} tools')
    assert len(tools) == 27

asyncio.run(test())
"
```

### Test 2: Reference Data

```bash
export BORSDATA_API_KEY="your_key"
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio
import json

async def test():
    server = BorsdataMCPServer()
    result = await server._call_tool_handler('get_markets', {})
    data = json.loads(result[0].text)
    print(f'Markets: {len(data)}')
    print(data[0] if data else 'No data')

asyncio.run(test())
"
```

### Test 3: Stock Prices

```bash
export BORSDATA_API_KEY="your_key"
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio
import json

async def test():
    server = BorsdataMCPServer()

    # Get an instrument
    result = await server._call_tool_handler('get_instruments', {})
    instruments = json.loads(result[0].text)
    inst_id = instruments[0]['ins_id']

    # Get prices
    result = await server._call_tool_handler('get_stock_prices', {
        'instrument_id': inst_id,
        'max_count': 5
    })
    prices = json.loads(result[0].text)
    print(f'Got {len(prices)} prices')
    print(prices[0] if prices else 'No data')

asyncio.run(test())
"
```

### Test 4: Error Cases

```bash
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio
import json

async def test():
    server = BorsdataMCPServer('invalid_key')

    # Should handle gracefully
    result = await server._call_tool_handler('unknown_tool', {})
    data = json.loads(result[0].text)
    print('Error response:', data)
    assert 'error' in data

asyncio.run(test())
"
```

## Interpreting Test Results

### Success Indicators

✅ **All tools registered**: Should see 27 tools  
✅ **No import errors**: Server starts without errors  
✅ **Valid responses**: Tools return properly formatted JSON  
✅ **Batch operations work**: Can query multiple instruments

### Common Issues

❌ **ModuleNotFoundError: No module named 'mcp'**  
→ Solution: `pip install mcp>=1.0.0`

❌ **API key required**  
→ Solution: `export BORSDATA_API_KEY="your_key"`

❌ **Rate limit exceeded**  
→ Solution: Wait a few seconds, tests include retry logic

❌ **Connection errors**  
→ Solution: Check internet connection, verify API is accessible

## Performance Testing

### Response Time Test

```bash
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio
import time

async def test():
    server = BorsdataMCPServer()

    start = time.time()
    result = await server._call_tool_handler('get_markets', {})
    elapsed = time.time() - start

    print(f'Response time: {elapsed:.3f}s')
    assert elapsed < 2.0, 'Too slow!'

asyncio.run(test())
"
```

### Batch vs Single Test

```bash
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio
import time
import json

async def test():
    server = BorsdataMCPServer()

    # Get instruments
    result = await server._call_tool_handler('get_instruments', {})
    instruments = json.loads(result[0].text)
    ids = [inst['ins_id'] for inst in instruments[:10]]

    # Test single calls
    start = time.time()
    for inst_id in ids[:3]:
        await server._call_tool_handler('get_stock_prices', {
            'instrument_id': inst_id,
            'max_count': 5
        })
    single_time = time.time() - start

    # Test batch call
    start = time.time()
    await server._call_tool_handler('get_stock_prices_batch', {
        'instrument_ids': ids[:3]
    })
    batch_time = time.time() - start

    print(f'Single calls: {single_time:.3f}s')
    print(f'Batch call: {batch_time:.3f}s')
    print(f'Speedup: {single_time/batch_time:.1f}x')

asyncio.run(test())
"
```

## Continuous Testing

### Pre-commit Tests

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd src/mcp_server
python test_server.py
if [ $? -ne 0 ]; then
    echo "MCP server tests failed!"
    exit 1
fi
```

### CI/CD Integration

For GitHub Actions:

```yaml
- name: Test MCP Server
  run: |
    cd src/mcp_server
    python test_server.py
  env:
    BORSDATA_API_KEY: ${{ secrets.BORSDATA_API_KEY }}
```

## Debugging

### Enable Verbose Output

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Tool Registration

```bash
python -c "
from mcp_server.server import BorsdataMCPServer
import asyncio

async def test():
    server = BorsdataMCPServer('test')
    tools = await server._list_tools_handler()
    for tool in tools:
        print(f'{tool.name}')
        print(f'  Schema: {tool.inputSchema}')
        print()

asyncio.run(test())
"
```

### Test Server Lifecycle

```bash
python -c "
from mcp_server.server import BorsdataMCPServer

print('Creating server...')
server = BorsdataMCPServer('test')
print('✅ Server created')

print('Getting client...')
client = server._get_client()
print('✅ Client initialized')
print(f'API key set: {bool(client.api_key)}')
"
```

## Next Steps

After testing locally:

1. **Verify with Claude Desktop** - The real-world test
2. **Check performance** - Ensure response times are acceptable
3. **Test edge cases** - Invalid IDs, missing data, etc.
4. **Monitor API usage** - Stay within rate limits
5. **Document issues** - Keep track of any problems

## Support

If tests fail:

1. Check the error message in `test_server.py` output
2. Verify API key is valid
3. Check network connectivity
4. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
5. See [USAGE_GUIDE.md](USAGE_GUIDE.md) for tool usage

## Test Checklist

Before deploying to production:

- [ ] `test_server.py` passes all tests
- [ ] Server starts without errors
- [ ] All 27 tools are registered
- [ ] Can retrieve instruments
- [ ] Can get stock prices
- [ ] Batch operations work
- [ ] Error handling is graceful
- [ ] Works with Claude Desktop
- [ ] Response times are acceptable
- [ ] Rate limiting is respected

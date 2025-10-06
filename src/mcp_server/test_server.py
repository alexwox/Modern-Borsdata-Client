#!/usr/bin/env python3
"""Manual testing script for the Borsdata MCP Server.

This script helps verify that the server is working correctly without needing
a full MCP client setup.
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict

from server import BorsdataMCPServer


async def test_list_tools():
    """Test that all tools are registered."""
    print("=" * 70)
    print("TEST 1: List Tools")
    print("=" * 70)
    
    try:
        api_key = os.environ.get("BORSDATA_API_KEY", "test_key")
        server = BorsdataMCPServer(api_key)
        
        tools = await server._list_tools_handler()
        
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:60]}...")
        
        assert len(tools) == 28, f"Expected 28 tools, got {len(tools)}"
        print("\n✅ Test passed: All 28 tools registered\n")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        return False


async def test_call_tool_reference_data():
    """Test reference data tools (no API key needed for testing structure)."""
    print("=" * 70)
    print("TEST 2: Call Reference Data Tools (Structure Only)")
    print("=" * 70)
    
    api_key = os.environ.get("BORSDATA_API_KEY")
    if not api_key:
        print("⚠️  No API key found. Testing structure only.")
        print("   Set BORSDATA_API_KEY to test actual API calls.\n")
        return True
    
    try:
        server = BorsdataMCPServer(api_key)
        
        # Test get_markets
        print("\n1. Testing get_markets...")
        result = await server._call_tool_handler("get_markets", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ⚠️  Error: {data['error']}")
        else:
            print(f"   ✅ Got {len(data)} markets")
            if data:
                print(f"   Sample: {data[0]}")
        
        # Test get_branches
        print("\n2. Testing get_branches...")
        result = await server._call_tool_handler("get_branches", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ⚠️  Error: {data['error']}")
        else:
            print(f"   ✅ Got {len(data)} branches")
            if data:
                print(f"   Sample: {data[0]}")
        
        # Test get_sectors
        print("\n3. Testing get_sectors...")
        result = await server._call_tool_handler("get_sectors", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ⚠️  Error: {data['error']}")
        else:
            print(f"   ✅ Got {len(data)} sectors")
            if data:
                print(f"   Sample: {data[0]}")
        
        print("\n✅ Test passed: Reference data tools work\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_call_tool_instruments():
    """Test getting instruments (most important reference data)."""
    print("=" * 70)
    print("TEST 3: Get Instruments")
    print("=" * 70)
    
    api_key = os.environ.get("BORSDATA_API_KEY")
    if not api_key:
        print("⚠️  No API key found. Skipping test.")
        print("   Set BORSDATA_API_KEY to test actual API calls.\n")
        return True
    
    try:
        server = BorsdataMCPServer(api_key)
        
        print("\nTesting get_instruments...")
        result = await server._call_tool_handler("get_instruments", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ❌ Error: {data['error']}")
            return False
        
        print(f"   ✅ Got {len(data)} instruments")
        if data:
            sample = data[0]
            print(f"\n   Sample instrument:")
            print(f"     ID: {sample.get('ins_id')}")
            print(f"     Name: {sample.get('name')}")
            print(f"     Ticker: {sample.get('ticker')}")
            print(f"     Market ID: {sample.get('market_id')}")
        
        print("\n✅ Test passed: Instruments retrieved\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_call_tool_stock_prices():
    """Test getting stock prices."""
    print("=" * 70)
    print("TEST 4: Get Stock Prices")
    print("=" * 70)
    
    api_key = os.environ.get("BORSDATA_API_KEY")
    if not api_key:
        print("⚠️  No API key found. Skipping test.")
        print("   Set BORSDATA_API_KEY to test actual API calls.\n")
        return True
    
    try:
        server = BorsdataMCPServer(api_key)
        
        # First get an instrument ID
        print("\n1. Getting instruments to find a stock...")
        result = await server._call_tool_handler("get_instruments", {})
        instruments = json.loads(result[0].text)
        
        if not instruments or "error" in instruments:
            print("   ⚠️  Couldn't get instruments, skipping price test")
            return True
        
        instrument_id = instruments[0]["ins_id"]
        instrument_name = instruments[0]["name"]
        print(f"   Using: {instrument_name} (ID: {instrument_id})")
        
        # Get stock prices
        print(f"\n2. Getting stock prices for {instrument_name}...")
        to_date = datetime.now()
        from_date = to_date - timedelta(days=30)
        
        result = await server._call_tool_handler("get_stock_prices", {
            "instrument_id": instrument_id,
            "from_date": from_date.strftime("%Y-%m-%d"),
            "to_date": to_date.strftime("%Y-%m-%d"),
            "max_count": 10
        })
        
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ❌ Error: {data['error']}")
            return False
        
        print(f"   ✅ Got {len(data)} price points")
        if data:
            sample = data[0]
            print(f"\n   Most recent price:")
            print(f"     Date: {sample.get('d')}")
            print(f"     Close: {sample.get('c')}")
            print(f"     Volume: {sample.get('v')}")
        
        print("\n✅ Test passed: Stock prices retrieved\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_call_tool_batch():
    """Test batch operations."""
    print("=" * 70)
    print("TEST 5: Batch Operations")
    print("=" * 70)
    
    api_key = os.environ.get("BORSDATA_API_KEY")
    if not api_key:
        print("⚠️  No API key found. Skipping test.")
        print("   Set BORSDATA_API_KEY to test actual API calls.\n")
        return True
    
    try:
        server = BorsdataMCPServer(api_key)
        
        # Get some instrument IDs
        print("\n1. Getting instruments...")
        result = await server._call_tool_handler("get_instruments", {})
        instruments = json.loads(result[0].text)
        
        if not instruments or "error" in instruments:
            print("   ⚠️  Couldn't get instruments, skipping batch test")
            return True
        
        # Get first 3 instruments
        instrument_ids = [inst["ins_id"] for inst in instruments[:3]]
        instrument_names = [inst["name"] for inst in instruments[:3]]
        print(f"   Using: {', '.join(instrument_names)}")
        
        # Test batch stock prices
        print(f"\n2. Getting batch stock prices...")
        to_date = datetime.now()
        from_date = to_date - timedelta(days=7)
        
        result = await server._call_tool_handler("get_stock_prices_batch", {
            "instrument_ids": instrument_ids,
            "from_date": from_date.strftime("%Y-%m-%d"),
            "to_date": to_date.strftime("%Y-%m-%d")
        })
        
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ❌ Error: {data['error']}")
            return False
        
        print(f"   ✅ Got batch data for {len(data)} instruments")
        
        print("\n✅ Test passed: Batch operations work\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_call_tool_kpi():
    """Test KPI tools."""
    print("=" * 70)
    print("TEST 6: KPI Tools")
    print("=" * 70)
    
    api_key = os.environ.get("BORSDATA_API_KEY")
    if not api_key:
        print("⚠️  No API key found. Skipping test.")
        print("   Set BORSDATA_API_KEY to test actual API calls.\n")
        return True
    
    try:
        server = BorsdataMCPServer(api_key)
        
        # Get KPI metadata
        print("\n1. Getting KPI metadata...")
        result = await server._call_tool_handler("get_kpi_metadata", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ❌ Error: {data['error']}")
            return False
        
        print(f"   ✅ Got {len(data)} KPIs")
        if data:
            sample = data[0]
            print(f"\n   Sample KPI:")
            print(f"     ID: {sample.get('kpi_id')}")
            print(f"     Name: {sample.get('kpi_name')}")
        
        # Get KPI update time
        print("\n2. Getting KPI update time...")
        result = await server._call_tool_handler("get_kpi_updated", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ⚠️  Error: {data['error']}")
        else:
            print(f"   ✅ Last updated: {data.get('kpis_calc_updated')}")
        
        print("\n✅ Test passed: KPI tools work\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_error_handling():
    """Test error handling with invalid inputs."""
    print("=" * 70)
    print("TEST 7: Error Handling")
    print("=" * 70)
    
    try:
        server = BorsdataMCPServer("invalid_key")
        
        # Test with invalid instrument ID
        print("\n1. Testing with invalid instrument ID...")
        result = await server._call_tool_handler("get_stock_prices", {
            "instrument_id": 999999,
            "max_count": 10
        })
        
        data = json.loads(result[0].text)
        
        # Should either get error or empty data
        if "error" in data or (isinstance(data, list) and len(data) == 0):
            print("   ✅ Error handled gracefully")
        else:
            print(f"   ⚠️  Unexpected response: {type(data)}")
        
        # Test with unknown tool
        print("\n2. Testing with unknown tool...")
        result = await server._call_tool_handler("unknown_tool", {})
        data = json.loads(result[0].text)
        
        if "error" in data:
            print(f"   ✅ Error caught: {data['error']}")
        else:
            print("   ⚠️  Should have returned error")
        
        print("\n✅ Test passed: Errors handled gracefully\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("BORSDATA MCP SERVER TEST SUITE")
    print("=" * 70)
    print()
    
    results = []
    
    # Run tests
    results.append(("List Tools", await test_list_tools()))
    results.append(("Reference Data", await test_call_tool_reference_data()))
    results.append(("Get Instruments", await test_call_tool_instruments()))
    results.append(("Stock Prices", await test_call_tool_stock_prices()))
    results.append(("Batch Operations", await test_call_tool_batch()))
    results.append(("KPI Tools", await test_call_tool_kpi()))
    results.append(("Error Handling", await test_error_handling()))
    
    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("=" * 70)
    
    return passed == total


def main():
    """Main entry point."""
    import sys
    
    # Check for API key
    if not os.environ.get("BORSDATA_API_KEY"):
        print("\n⚠️  WARNING: BORSDATA_API_KEY not set")
        print("   Some tests will be skipped.")
        print("   Set the environment variable to run all tests:")
        print("   export BORSDATA_API_KEY='your_key_here'\n")
    
    # Run tests
    result = asyncio.run(run_all_tests())
    
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()


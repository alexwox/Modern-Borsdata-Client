#!/usr/bin/env python3
"""
Basic usage example for the Borsdata API client.

This example demonstrates how to use the client to fetch basic data from the Borsdata API.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from borsdata_client import BorsdataClient

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("BORSDATA_API_KEY")
if not api_key:
    raise ValueError("BORSDATA_API_KEY environment variable not set")

def main():
    """Run the example."""
    # Use the client as a context manager
    with BorsdataClient(api_key) as client:
        # Get all instruments
        print("Fetching instruments...")
        instruments = client.get_instruments()
        print(f"Found {len(instruments)} instruments")
        
        # Get markets
        print("\nFetching markets...")
        markets = client.get_markets()
        print(f"Found {len(markets)} markets:")
        for market in markets:
            print(f"  - {market.name} (ID: {market.id})")
        
        # Get stock prices for a specific instrument (using the first one as an example)
        if instruments:
            instrument = instruments[0]
            print(f"\nFetching stock prices for {instrument.name}...")
            
            today = datetime.now()
            one_month_ago = today - timedelta(days=30)
            
            prices = client.get_stock_prices(
                instrument_id=instrument.ins_id,
                from_date=one_month_ago,
                to_date=today
            )
            
            print(f"Found {len(prices)} price points:")
            for i, price in enumerate(prices[:5]):  # Show only first 5 prices
                print(f"  - {price.d}: Close: {price.c}, Volume: {price.v}")
            
            if len(prices) > 5:
                print(f"  ... and {len(prices) - 5} more")

if __name__ == "__main__":
    main() 
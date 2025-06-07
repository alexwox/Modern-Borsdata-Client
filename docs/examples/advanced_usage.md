# Advanced Usage Examples

This document provides advanced usage examples for the BorsdataClient library.

## Working with Multiple Instruments

```python
from borsdata_client import BorsdataClient
import os
from datetime import datetime

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key, retry=True, max_retries=5) as client:
    # Get all instruments
    instruments = client.get_instruments()

    # Filter instruments by market
    stockholm_instruments = [i for i in instruments if i.market_id == 1]  # Stockholm

    # Get last stock prices for all instruments (more efficient than querying each)
    last_prices = client.get_last_stock_prices()

    # Create a dictionary mapping instrument IDs to their last prices
    price_map = {price.i: price for price in last_prices}

    # Print instruments with their last prices
    for instrument in stockholm_instruments[:10]:  # First 10 Stockholm instruments
        if instrument.ins_id in price_map:
            price = price_map[instrument.ins_id]
            print(f"{instrument.name} ({instrument.ticker}): {price.c} {instrument.stock_price_currency}")
```

## Analyzing Financial Data

```python
from borsdata_client import BorsdataClient
import os
import pandas as pd
from datetime import datetime

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get all instruments
    instruments = client.get_instruments()

    # Get P/E ratios for multiple companies
    target_instruments = [3, 4, 5]  # Example IDs
    pe_data = []

    for ins_id in target_instruments:
        kpi_history = client.get_kpi_history(
            instrument_id=ins_id,
            kpi_id=1,  # P/E ratio
            report_type="year",
            max_count=5
        )

        # Find the instrument name
        instrument_name = next((i.name for i in instruments if i.ins_id == ins_id), f"Unknown ({ins_id})")

        # Add data to list
        for value in kpi_history.values:
            pe_data.append({
                "Instrument ID": ins_id,
                "Name": instrument_name,
                "P/E Ratio": value.n
            })

    # Convert to pandas DataFrame for analysis
    df = pd.DataFrame(pe_data)

    # Calculate average P/E ratio by company
    avg_pe = df.groupby("Name")["P/E Ratio"].mean()
    print("Average P/E Ratios:")
    print(avg_pe)
```

## Tracking Insider Trading

```python
from borsdata_client import BorsdataClient
import os
from datetime import datetime, timedelta

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get all instruments
    instruments = client.get_instruments()

    # Create a mapping of instrument IDs to names
    instrument_map = {i.ins_id: i.name for i in instruments}

    # Get insider trading data for specific instruments
    target_instruments = [3, 4, 5]  # Example IDs
    insider_data = client.get_insider_holdings(target_instruments)

    # Find significant insider transactions (large amounts)
    significant_transactions = []

    for response in insider_data:
        for insider_list in response.list:
            ins_id = insider_list.ins_id
            instrument_name = instrument_map.get(ins_id, f"Unknown ({ins_id})")

            if insider_list.values:
                for transaction in insider_list.values:
                    # Filter for significant transactions (e.g., over 1,000,000 in value)
                    if transaction.amount > 1000000:
                        significant_transactions.append({
                            "Instrument": instrument_name,
                            "Owner": transaction.owner_name,
                            "Position": transaction.owner_position,
                            "Shares": transaction.shares,
                            "Amount": transaction.amount,
                            "Date": transaction.transaction_date
                        })

    # Print significant transactions
    for transaction in significant_transactions:
        print(f"Significant insider transaction in {transaction['Instrument']}:")
        print(f"  Owner: {transaction['Owner']} ({transaction['Position']})")
        print(f"  Shares: {transaction['Shares']}")
        print(f"  Amount: {transaction['Amount']}")
        print(f"  Date: {transaction['Date']}")
        print("---")
```

## Monitoring Upcoming Reports

```python
from borsdata_client import BorsdataClient
import os
from datetime import datetime, timedelta

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get all instruments
    instruments = client.get_instruments()

    # Create a mapping of instrument IDs to names
    instrument_map = {i.ins_id: i.name for i in instruments}

    # Get report calendar for specific instruments
    target_instruments = [3, 4, 5, 6, 7, 8, 9, 10]  # Example IDs
    report_calendar = client.get_report_calendar(target_instruments)

    # Find upcoming reports in the next 30 days
    today = datetime.now()
    next_month = today + timedelta(days=30)
    upcoming_reports = []

    for response in report_calendar:
        for calendar in response.list:
            ins_id = calendar.ins_id
            instrument_name = instrument_map.get(ins_id, f"Unknown ({ins_id})")

            if calendar.values:
                for date in calendar.values:
                    # Filter for upcoming reports
                    if today <= date.release_date <= next_month:
                        upcoming_reports.append({
                            "Instrument": instrument_name,
                            "Release Date": date.release_date,
                            "Report Type": date.report_type
                        })

    # Sort by release date
    upcoming_reports.sort(key=lambda x: x["Release Date"])

    # Print upcoming reports
    print(f"Upcoming reports in the next 30 days ({today.strftime('%Y-%m-%d')} to {next_month.strftime('%Y-%m-%d')}):")
    for report in upcoming_reports:
        print(f"{report['Release Date'].strftime('%Y-%m-%d')}: {report['Instrument']} - {report['Report Type']}")
```

## Analyzing Stock Price Trends

```python
from borsdata_client import BorsdataClient
import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get stock prices for the last year
    today = datetime.now()
    last_year = today - timedelta(days=365)

    # Get stock prices for multiple instruments
    target_instruments = [3, 4, 5]  # Example IDs: Volvo B, etc.

    # Get instrument names
    instruments = client.get_instruments()
    instrument_map = {i.ins_id: i.name for i in instruments}

    # Create a DataFrame to store all price data
    all_prices = pd.DataFrame()

    for ins_id in target_instruments:
        prices = client.get_stock_prices(
            instrument_id=ins_id,
            from_date=last_year,
            to_date=today
        )

        # Convert to DataFrame
        df = pd.DataFrame([{
            "Date": p.get_date(),
            "Close": p.c,
            "Instrument": instrument_map.get(ins_id, f"Unknown ({ins_id})")
        } for p in prices])

        # Append to all_prices
        all_prices = pd.concat([all_prices, df])

    # Pivot the DataFrame for plotting
    pivot_df = all_prices.pivot(index="Date", columns="Instrument", values="Close")

    # Normalize to starting value (100%)
    normalized_df = pivot_df / pivot_df.iloc[0] * 100

    # Plot the normalized stock prices
    normalized_df.plot(figsize=(12, 6), title="Normalized Stock Price Performance (Last Year)")
    plt.ylabel("Price (% of starting value)")
    plt.grid(True)
    plt.savefig("stock_performance.png")
    plt.close()

    print("Stock price performance chart saved as 'stock_performance.png'")
```

## Combining Multiple Data Sources

```python
from borsdata_client import BorsdataClient
import os
from datetime import datetime, timedelta
import pandas as pd

api_key = os.environ.get("BORSDATA_API_KEY")

with BorsdataClient(api_key) as client:
    # Get all instruments
    instruments = client.get_instruments()

    # Get all branches
    branches = client.get_branches()
    branch_map = {b.id: b.name for b in branches}

    # Create a DataFrame with instrument details
    instrument_df = pd.DataFrame([{
        "ID": i.ins_id,
        "Name": i.name,
        "Ticker": i.ticker,
        "Branch ID": i.branch_id,
        "Branch": branch_map.get(i.branch_id, "Unknown") if i.branch_id else "Unknown"
    } for i in instruments])

    # Get last stock prices
    last_prices = client.get_last_stock_prices()

    # Create a DataFrame with price details
    price_df = pd.DataFrame([{
        "ID": p.i,
        "Date": datetime.strptime(p.d, "%Y-%m-%d"),
        "Close": p.c,
        "Volume": p.v
    } for p in last_prices])

    # Merge the DataFrames
    combined_df = pd.merge(instrument_df, price_df, on="ID", how="left")

    # Group by branch and calculate average price
    branch_stats = combined_df.groupby("Branch").agg({
        "Close": ["mean", "min", "max", "count"],
        "Volume": ["mean", "sum"]
    })

    # Print branch statistics
    print("Branch Statistics:")
    print(branch_stats)

    # Find the branch with the highest average price
    highest_avg_price_branch = branch_stats["Close"]["mean"].idxmax()
    print(f"\nBranch with highest average price: {highest_avg_price_branch}")

    # Find the branch with the highest trading volume
    highest_volume_branch = branch_stats["Volume"]["sum"].idxmax()
    print(f"Branch with highest trading volume: {highest_volume_branch}")
```

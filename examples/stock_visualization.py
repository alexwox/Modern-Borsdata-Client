#!/usr/bin/env python3
"""
Stock visualization example using the Borsdata API client.

This example demonstrates how to create beautiful visualizations of stock data
including price trends, volume, and basic technical indicators.
"""

import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from borsdata_client import BorsdataClient

# Set style for prettier plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("BORSDATA_API_KEY")
if not api_key:
    raise ValueError("BORSDATA_API_KEY environment variable not set")

def get_stock_data(client: BorsdataClient, ticker: str, days: int = 365) -> pd.DataFrame:
    """
    Fetch stock data and convert it to a pandas DataFrame.
    
    Args:
        client: BorsdataClient instance
        ticker: Stock ticker symbol
        days: Number of days of historical data to fetch
        
    Returns:
        DataFrame with stock price data
    """
    # Find the instrument
    instruments = client.get_instruments()
    instrument = next((i for i in instruments if i.ticker == ticker), None)
    if not instrument:
        raise ValueError(f"Could not find instrument with ticker {ticker}")
    
    # Get historical prices
    today = datetime.now()
    start_date = today - timedelta(days=days)
    prices = client.get_stock_prices(
        instrument_id=instrument.ins_id,
        from_date=start_date,
        to_date=today
    )
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'Date': datetime.strptime(p.d, '%Y-%m-%d'),
        'Open': p.o,
        'High': p.h,
        'Low': p.l,
        'Close': p.c,
        'Volume': p.v
    } for p in prices])
    
    df.set_index('Date', inplace=True)
    
    # Add some technical indicators
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['Daily_Return'] = df['Close'].pct_change()
    
    return df

def plot_stock_analysis(df: pd.DataFrame, ticker: str):
    """
    Create a comprehensive visualization of stock data.
    
    Args:
        df: DataFrame with stock price data
        ticker: Stock ticker symbol for the title
    """
    # Create a figure with subplots
    fig = plt.figure(figsize=(16, 10), constrained_layout=True)
    
    # Define grid for subplots
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])
    
    # Price and Moving Averages
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df.index, df['Close'], label='Close Price', linewidth=1.5)
    ax1.plot(df.index, df['SMA_20'], label='20-day SMA', linestyle='--', alpha=0.8)
    ax1.plot(df.index, df['SMA_50'], label='50-day SMA', linestyle='--', alpha=0.8)
    ax1.set_title(f'{ticker} Stock Price Analysis', fontsize=14, pad=20)
    ax1.set_ylabel('Price')
    ax1.legend(loc='center left', bbox_to_anchor=(1.02, 0.5),
              fancybox=True, shadow=True, framealpha=1)
    ax1.grid(True, alpha=0.3)
    
    # Volume
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.bar(df.index, df['Volume'], alpha=0.5, color='darkblue')
    ax2.set_ylabel('Volume')
    ax2.grid(True, alpha=0.3)
    
    # Daily Returns
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(df.index, df['Daily_Return'], color='green', alpha=0.7)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.fill_between(df.index, df['Daily_Return'], 0, 
                     where=(df['Daily_Return'] >= 0), color='green', alpha=0.3)
    ax3.fill_between(df.index, df['Daily_Return'], 0, 
                     where=(df['Daily_Return'] < 0), color='red', alpha=0.3)
    ax3.set_ylabel('Daily Returns')
    ax3.grid(True, alpha=0.3)
    
    # Adjust layout and display
    plt.xlabel('Date')
    
    # Add some statistics as text
    stats_text = (
        f"Statistics:\n"
        f"Current Price: {df['Close'].iloc[-1]:.2f}\n"
        f"52-week High: {df['High'].max():.2f}\n"
        f"52-week Low: {df['Low'].min():.2f}\n"
        f"Daily Vol.: {df['Daily_Return'].std()*100:.2f}%"
    )
    
    # Add text in a better position that won't conflict with tight_layout
    ax1.text(0.02, 0.98, stats_text,
             transform=ax1.transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'),
             fontsize=10,
             verticalalignment='top')
    
    return fig

def main():
    """Run the stock visualization example."""
    # Example tickers (can be changed to any stock available in Borsdata)
    tickers = ['ERIC B', 'VOLV B']
    
    with BorsdataClient(api_key) as client:
        for ticker in tickers:
            try:
                print(f"\nFetching data for {ticker}...")
                df = get_stock_data(client, ticker)
                
                print("Creating visualization...")
                fig = plot_stock_analysis(df, ticker)
                
                # Save the plot
                filename = f"{ticker.replace(' ', '_')}_analysis.png"
                fig.savefig(filename)
                print(f"Saved visualization to {filename}")
                plt.close(fig)
                
            except Exception as e:
                print(f"Error processing {ticker}: {e}")

if __name__ == "__main__":
    main() 
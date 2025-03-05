#!/usr/bin/env python3
"""
Portfolio analysis example using the Borsdata API client.

This example demonstrates how to use the client to analyze a portfolio of stocks.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
from dotenv import load_dotenv
from borsdata_client import BorsdataClient, Instrument, StockPrice

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("BORSDATA_API_KEY")
if not api_key:
    raise ValueError("BORSDATA_API_KEY environment variable not set")

# Define a sample portfolio (ticker: number of shares)
PORTFOLIO = {
    "ERIC B": 100,  # Ericsson
    "VOLV B": 50,   # Volvo
    "SEB A": 75,    # SEB
}

def get_instrument_by_ticker(client: BorsdataClient, ticker: str) -> Instrument:
    """Find an instrument by its ticker symbol."""
    instruments = client.get_instruments()
    for instrument in instruments:
        if instrument.ticker == ticker:
            return instrument
    raise ValueError(f"Instrument with ticker {ticker} not found")

def get_historical_prices(
    client: BorsdataClient, 
    instrument_id: int, 
    days: int = 365
) -> List[StockPrice]:
    """Get historical prices for an instrument."""
    today = datetime.now()
    start_date = today - timedelta(days=days)
    
    return client.get_stock_prices(
        instrument_id=instrument_id,
        from_date=start_date,
        to_date=today
    )

def calculate_portfolio_value(
    client: BorsdataClient,
    portfolio: Dict[str, int]
) -> Tuple[float, Dict[str, float], pd.DataFrame]:
    """Calculate the current value of a portfolio and its performance."""
    total_value = 0.0
    stock_values = {}
    price_history = {}
    
    # Get data for each stock in the portfolio
    for ticker, shares in portfolio.items():
        try:
            # Get the instrument
            instrument = get_instrument_by_ticker(client, ticker)
            
            # Get historical prices
            prices = get_historical_prices(client, instrument.insId)
            
            if not prices:
                print(f"No price data available for {ticker}")
                continue
                
            # Get the latest price
            latest_price = prices[-1].c
            stock_value = latest_price * shares
            
            # Store the results
            total_value += stock_value
            stock_values[ticker] = stock_value
            
            # Create a time series of prices
            dates = [price.d for price in prices]
            close_prices = [price.c for price in prices]
            price_history[ticker] = pd.Series(close_prices, index=dates)
            
            print(f"{ticker}: {shares} shares at {latest_price:.2f} = {stock_value:.2f}")
            
        except ValueError as e:
            print(f"Error processing {ticker}: {e}")
    
    # Create a DataFrame with all price histories
    df = pd.DataFrame(price_history)
    
    # Calculate portfolio value over time (weighted by shares)
    portfolio_weights = {}
    for ticker, shares in portfolio.items():
        if ticker in df.columns:
            portfolio_weights[ticker] = shares
    
    # Calculate weighted sum
    if portfolio_weights:
        df['Portfolio'] = sum(df[ticker] * shares for ticker, shares in portfolio_weights.items())
    
    return total_value, stock_values, df

def main():
    """Run the portfolio analysis example."""
    with BorsdataClient(api_key) as client:
        print("Analyzing portfolio...")
        total_value, stock_values, price_history = calculate_portfolio_value(client, PORTFOLIO)
        
        print("\nPortfolio Summary:")
        print(f"Total Value: {total_value:.2f}")
        
        print("\nAllocation:")
        for ticker, value in stock_values.items():
            percentage = (value / total_value) * 100 if total_value > 0 else 0
            print(f"  {ticker}: {value:.2f} ({percentage:.2f}%)")
        
        # Calculate performance metrics if we have data
        if not price_history.empty and 'Portfolio' in price_history.columns:
            portfolio_series = price_history['Portfolio']
            
            # Calculate returns
            returns = portfolio_series.pct_change().dropna()
            
            print("\nPerformance Metrics:")
            print(f"  Start Value: {portfolio_series.iloc[0]:.2f}")
            print(f"  End Value: {portfolio_series.iloc[-1]:.2f}")
            
            total_return = (portfolio_series.iloc[-1] / portfolio_series.iloc[0] - 1) * 100
            print(f"  Total Return: {total_return:.2f}%")
            
            annualized_return = ((1 + total_return/100) ** (365/len(portfolio_series)) - 1) * 100
            print(f"  Annualized Return: {annualized_return:.2f}%")
            
            volatility = returns.std() * (252 ** 0.5) * 100  # Annualized volatility
            print(f"  Volatility (Annualized): {volatility:.2f}%")
            
            if volatility > 0:
                sharpe = annualized_return / volatility  # Simplified Sharpe ratio (no risk-free rate)
                print(f"  Sharpe Ratio: {sharpe:.2f}")

if __name__ == "__main__":
    main() 
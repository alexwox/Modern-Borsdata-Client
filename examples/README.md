# Borsdata Client Examples

This directory contains example scripts demonstrating how to use the Borsdata API client.

## Prerequisites

Before running these examples, make sure you have:

1. Clone the repository and install the package in development mode:

   ```bash
   # Clone the repository
   git clone https://github.com/alexwox/Modern-Borsdata-Client.git
   cd Modern-Borsdata-Client

   # Create and activate a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

   # Install basic dependencies
   pip install -e .

   # For running all examples including visualization
   pip install -r requirements-dev.txt
   ```

2. Set up your API key as an environment variable or in a `.env` file:
   ```
   BORSDATA_API_KEY=your_api_key_here
   ```

## Examples

### Basic Usage (`basic_usage.py`)

A simple example showing how to fetch basic data from the Borsdata API:

- List all available instruments
- Get market information
- Fetch historical stock prices

```bash
python basic_usage.py
```

### Portfolio Analysis (`portfolio_analysis.py`)

An advanced example demonstrating portfolio analysis capabilities:

- Track multiple stocks in a portfolio
- Calculate total portfolio value
- Analyze portfolio allocation
- Calculate key performance metrics:
  - Total and annualized returns
  - Portfolio volatility
  - Sharpe ratio

```bash
python portfolio_analysis.py
```

### Stock Visualization (`stock_visualization.py`)

A comprehensive visualization tool that creates beautiful charts for stock analysis:

- Interactive price charts with multiple views:
  - Price trends with 20-day and 50-day moving averages
  - Trading volume analysis
  - Daily returns visualization with color-coded gains/losses
- Key statistics display including:
  - Current price
  - 52-week high/low
  - Daily volatility
- Generates high-quality PNG files for each analyzed stock

```bash
python stock_visualization.py
```

## Dependencies

Each example may require different dependencies:

- `basic_usage.py`: Basic requirements only
- `portfolio_analysis.py`: Requires pandas
- `stock_visualization.py`: Requires pandas, matplotlib, and seaborn

All required dependencies are included in `requirements-dev.txt`.

## Customizing the Examples

These examples are designed to be easily customizable:

### Basic Usage

- Modify the time period for historical data
- Change the number of price points displayed

### Portfolio Analysis

- Edit the `PORTFOLIO` dictionary to include your stocks
- Adjust the analysis period
- Add custom performance metrics

### Stock Visualization

- Modify the `tickers` list to analyze different stocks
- Customize the chart appearance:
  - Change colors and styles
  - Adjust technical indicators
  - Modify the layout
- Add additional technical indicators
- Change the time period (default is 1 year)

## Output Examples

- `basic_usage.py`: Prints data to console
- `portfolio_analysis.py`: Displays portfolio statistics and performance metrics
- `stock_visualization.py`: Generates `{TICKER}_analysis.png` files with comprehensive visualizations

## Error Handling

All examples include proper error handling for common issues:

- Missing API key
- Invalid stock tickers
- Network connection problems
- Missing data

## Contributing

Feel free to contribute additional examples or improvements to existing ones through pull requests.

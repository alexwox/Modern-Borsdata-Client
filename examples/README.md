# Borsdata Client Examples

This directory contains example scripts demonstrating how to use the Borsdata API client.

## Prerequisites

Before running these examples, make sure you have:

1. Installed the borsdata-client package:

   ```bash
   pip install borsdata-client
   ```

2. Set up your API key as an environment variable or in a `.env` file:
   ```
   BORSDATA_API_KEY=your_api_key_here
   ```

## Examples

### Basic Usage (`basic_usage.py`)

A simple example showing how to fetch instruments, markets, and stock prices.

```bash
python basic_usage.py
```

### Portfolio Analysis (`portfolio_analysis.py`)

A more advanced example demonstrating how to analyze a portfolio of stocks.

**Additional Requirements:**

- pandas: `pip install pandas`

```bash
python portfolio_analysis.py
```

## Customizing the Examples

Feel free to modify these examples to suit your needs. You can:

- Change the portfolio stocks in `portfolio_analysis.py`
- Adjust the time periods for historical data
- Add additional analysis metrics
- Integrate with visualization libraries like matplotlib or plotly

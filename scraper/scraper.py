import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz


def get_data(tickers, days_back=60):
    """
    Fetch global stock/index data
    Args:
        tickers: List of verified ticker symbols
        days_back: Number of days of historical data (1-365)
    Returns:
        DataFrame with columns: Ticker, Date (IST), Price
    """
    # Validate inputs
    if not isinstance(tickers, list):
        raise ValueError("tickers must be a list")
    if len(tickers) == 0:
        raise ValueError("tickers list cannot be empty")
    if not 1 <= days_back <= 10000:
        raise ValueError("days_back must be between 1-10,000")

    # Download data with error handling
    try:
        data = yf.download(
            tickers,
            period=f"{days_back}d",
            group_by='ticker',
            auto_adjust=True,
            progress=False,
            threads=True
        )
    except Exception as e:
        raise ValueError(f"Download failed: {str(e)}")

    # Process each ticker with validation
    dfs = []
    valid_tickers = []
    for ticker in tickers:
        if ticker in data:
            df = data[ticker][['Close']].copy()
            df['Ticker'] = ticker
            dfs.append(df)
            valid_tickers.append(ticker)
        else:
            print(f"⚠️ No data for {ticker} - possibly delisted or invalid")

    if not dfs:
        raise ValueError("No valid data retrieved - check ticker symbols")

    print(f"Successfully retrieved data for {len(valid_tickers)}/{len(tickers)} tickers")

    # Combine and clean data
    combined = pd.concat(dfs).reset_index()
    combined.rename(columns={'Close': 'Price', 'Date': 'Datetime_UTC'}, inplace=True)

    # Convert to IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    combined['Date'] = (
        pd.to_datetime(combined['Datetime_UTC'])
        .dt.tz_localize('UTC')
        .dt.tz_convert(ist)
        .dt.date
    )

    return combined[['Ticker', 'Date', 'Price']].dropna()


if __name__ == "__main__":
    try:
        print("Testing with verified assets...")
        test_data = get_data(["AAPL", "MSFT", "GOOGL"], days_back=7)
        print("\nSample Data:")
        print(test_data.head(3))
        print(f"\nDate Range: {test_data['Date'].min()} to {test_data['Date'].max()}")
    except Exception as e:
        print(f"\nError: {str(e)}")
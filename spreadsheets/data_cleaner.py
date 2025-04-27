import pandas as pd


def clean_data(df):
    """
    Clean global market data
    Args:
        df: DataFrame with columns ['Ticker', 'Date', 'Price']
    Returns:
        Cleaned DataFrame
    """
    cleaned = df.copy()

    # Ensure proper data types
    cleaned['Date'] = pd.to_datetime(cleaned['Date'])
    cleaned['Price'] = pd.to_numeric(cleaned['Price'], errors='coerce')

    # Remove rows with missing values
    cleaned = cleaned.dropna()

    # Remove duplicates
    cleaned = cleaned.drop_duplicates(['Ticker', 'Date'])

    # Sort by Ticker and Date
    return cleaned.sort_values(['Ticker', 'Date']).reset_index(drop=True)


if __name__ == "__main__":
    test_data = pd.DataFrame({
        'Ticker': ['AAPL', 'AAPL', '^GSPC', '^GSPC'],
        'Date': ['2025-04-01', '2025-04-02', '2025-04-01', '2025-04-02'],
        'Price': [170.12, 171.34, 5200, 5250]
    })
    print("Cleaned Data:")
    print(clean_data(test_data))
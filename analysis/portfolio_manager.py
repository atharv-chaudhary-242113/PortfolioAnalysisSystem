import pandas as pd
import numpy as np


class PortfolioManager:
    def __init__(self, df):
        """
        Initialize with portfolio data
        Required columns: 'Ticker', 'Date', 'Price'
        """
        self.df = self._validate_data(df.copy())
        self._preprocess_data()

    def _validate_data(self, df):
        """Verify data structure and quality"""
        required_cols = {'Ticker', 'Date', 'Price'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"Missing columns: {missing}")

        if df.empty:
            raise ValueError("Empty DataFrame provided")

        return df

    def _preprocess_data(self):
        """Prepare data for analysis"""
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df.sort_values(['Ticker', 'Date'])

        # Calculate daily returns
        self.df['Daily_Return'] = self.df.groupby('Ticker')['Price'].pct_change()

    def get_summary(self):
        """
        Generate performance summary
        Returns DataFrame with metrics:
        - Ticker
        - Period (date range)
        - Return (%)
        - Volatility (annualized %)
        - Risk Days (negative return days)
        - Best/Worst Day (%)
        """
        summary = []

        for ticker in self.df['Ticker'].unique():
            ticker_data = self.df[self.df['Ticker'] == ticker].dropna()

            if len(ticker_data) < 2:
                continue

            returns = ticker_data['Daily_Return']
            start_price = ticker_data['Price'].iloc[0]
            end_price = ticker_data['Price'].iloc[-1]

            summary.append({
                'Ticker': ticker,
                'Start_Date': ticker_data['Date'].min().strftime('%Y-%m-%d'),
                'End_Date': ticker_data['Date'].max().strftime('%Y-%m-%d'),
                'Return_Pct': round((end_price / start_price - 1) * 100, 2),
                'Volatility_Pct': round(returns.std() * np.sqrt(252) * 100, 2),
                'Risk_Days': len(returns[returns < 0]),
                'Best_Day_Pct': round(returns.max() * 100, 2),
                'Worst_Day_Pct': round(returns.min() * 100, 2)
            })

        return pd.DataFrame(summary)


if __name__ == "__main__":
    # Test with sample data
    test_data = pd.DataFrame({
        'Ticker': ['AAPL', 'AAPL', 'MSFT', 'MSFT'],
        'Date': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-02'],
        'Price': [150.0, 152.5, 250.0, 248.0]
    })

    pm = PortfolioManager(test_data)
    print("Test Summary:")
    print(pm.get_summary().to_string(index=False))
import pandas as pd
import os
from datetime import datetime


class CSVHandler:
    def __init__(self, output_dir="data"):
        """
        Initialize CSV handler
        Args:
            output_dir: Directory to save CSV files
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_to_csv(self, df, filename):
        """
        Save DataFrame to CSV
        Args:
            df: Pandas DataFrame
            filename: Output filename (without extension)
        Returns:
            str: Full path to saved file
        """
        filepath = os.path.join(self.output_dir, f"{filename}")
        df.to_csv(filepath, index=False)
        return filepath

    def generate_filename(self, prefix="portfolio"):
        """Generate timestamped filename"""
        return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


if __name__ == "__main__":
    # Test functionality
    test_data = pd.DataFrame({
        'Ticker': ['AAPL', 'MSFT'],
        'Date': ['2025-04-01', '2025-04-02'],
        'Price': [170.12, 300.45]
    })

    handler = CSVHandler()
    filename = handler.generate_filename()
    saved_path = handler.save_to_csv(test_data, filename)
    print(f"Test data saved to: {saved_path}")
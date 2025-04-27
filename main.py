from scraper.scraper import get_data
from spreadsheets.data_cleaner import clean_data
from spreadsheets.csv_handler import CSVHandler
from database.db_handler import DBHandler
from analysis.portfolio_manager import PortfolioManager
from visuals.visuals import PortfolioVisuals
import pytz
from datetime import datetime
import sys

# Configuration
IST = pytz.timezone('Asia/Kolkata')
DEFAULT_TICKERS = ["^GSPC", "AAPL", "MSFT", "GOOGL"]
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "60635062021492",
    "database": "portfolio_db"
}


def get_ticker_groups():
    """Get predefined groups of tickers"""
    return {
        'S&P 500 (Top 30)': [
            'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK-B', 'JNJ', 'V', 'PG',
            'JPM', 'HD', 'MA', 'DIS', 'ADBE', 'PEP', 'NVDA', 'CRM', 'NFLX', 'PYPL',
            'INTC', 'CMCSA', 'CSCO', 'ABT', 'TMO', 'AVGO', 'COST', 'ACN', 'QCOM', 'TXN'
        ],
        'NASDAQ 100 (Top 30)': [
            'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'ADBE', 'CSCO', 'INTC',
            'CMCSA', 'PEP', 'AVGO', 'COST', 'TMUS', 'QCOM', 'TXN', 'AMGN', 'SBUX', 'MDLZ',
            'BKNG', 'ADP', 'GILD', 'REGN', 'CHTR', 'VRTX', 'ISRG', 'INTU', 'FISV', 'AMD'
        ],
        'Nifty 50 (India)': [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
            'ICICIBANK.NS', 'ITC.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'LT.NS',
            'SBIN.NS', 'BAJFINANCE.NS', 'HDFC.NS', 'ASIANPAINT.NS', 'HCLTECH.NS',
            'MARUTI.NS', 'TITAN.NS', 'WIPRO.NS', 'ONGC.NS', 'NTPC.NS'
        ],
        'Global Blue Chips': [
            'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'JNJ', 'V', 'PG', 'NESN.SW', 'TM',
            'SHEL', 'HSBC', 'NVS', 'UL', 'BHP', 'RIO', 'TTE', 'SNY', 'AZN', 'ASML'
        ],
        "Technology (US)": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"],
        "Finance (US)": ["JPM", "BAC", "WFC", "GS", "MS", "BRK.A"],
        "Energy (US)": ["XOM", "CVX", "SHEL", "TTE", "COP"],
        "Healthcare (US)": ["JNJ", "PFE", "MRK", "ABBV", "LLY"],
        "Indian Tech": ["INFY.NS", "TCS.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS"],
        "Indian Finance": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS"],
        "Global Tech": ["AAPL", "MSFT", "ASML", "TSM", "0700.HK"],  # Added ASML, TSMC, Tencent
        "Emerging Markets": ["EEM", "MSCI", "INDA", "MCHI", "EWZ"],  # Added an ETF and some country-specific ETFs
    }


def run_pipeline(tickers, days_back, log_callback=None, root=None, group_name="Custom"):
    """Run analysis pipeline with GUI support"""

    def log(message):
        if log_callback:
            log_callback(message)
        else:
            print(message)

    try:
        log(f"\n🕒 {get_ist_time()}")
        log(f"🚀 Starting {group_name} Portfolio Analysis")

        # 1. Data Collection
        log(f"\n🔎 Fetching {days_back} days data for {len(tickers)} tickers...")
        raw_data = get_data(tickers, days_back)
        log(f"Retrieved {len(raw_data)} records")
        log(f"Date Range: {raw_data['Date'].min()} to {raw_data['Date'].max()} IST")

        # 2. Data Preparation
        cleaned_data = clean_data(raw_data[['Ticker', 'Date', 'Price']])

        # 3. Storage
        log("\n💾 Saving to CSV...")
        csv_handler = CSVHandler()
        filename = f"{group_name.lower().replace(' ', '_')}_{datetime.now(IST).strftime('%Y%m%d_%H%M')}.csv"
        csv_path = csv_handler.save_to_csv(cleaned_data, filename)
        log(f"Saved to: {csv_path}")

        # 4. Database Upload
        log("\n📦 Uploading to MySQL...")
        db_handler = DBHandler(DB_CONFIG, root) # Ensure root is passed here as well
        if db_handler.upload_data(cleaned_data, group_name):
            log("✅ Database upload successful!")
        else:
            log("⚠️ Partial upload completed")

        # 5. Portfolio Analysis
        log("\n📊 Running Analysis...")
        pm = PortfolioManager(cleaned_data)
        portfolio_summary = pm.get_summary()

        # 6. Visualization
        log("\n📈 Generating Visualizations...")
        visuals = PortfolioVisuals(cleaned_data, root)
        visuals.plot_chart()  # Call the plot_chart method here
        visuals.show_summary_table(portfolio_summary)

        log(f"\n✅ {group_name} analysis completed at {get_ist_time()}")
        return cleaned_data # Return the cleaned_data

    except Exception as e:
        log(f"\n❌ Pipeline failed at {get_ist_time()}")
        log(f"Error: {str(e)}")
        return None # Return None in case of an error


def get_ist_time():
    """Get formatted IST timestamp"""
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S %Z")


def main():
    """Command-line interface"""
    try:
        # Initialize database tables
        db_handler = DBHandler(DB_CONFIG)
        db_handler.initialize_tables()

        print("Portfolio Analysis System - Command Line Mode")
        groups = get_ticker_groups()

        print("\nAvailable Groups:")
        for i, (name, tickers) in enumerate(groups.items(), 1):
            print(f"{i}. {name} ({len(tickers)} tickers)")

        choice = input("\nEnter group number (1-4), symbols (comma separated), or press Enter for default: ").strip()

        if not choice:
            tickers = DEFAULT_TICKERS
            group_name = "Custom"
        elif choice.isdigit() and 1 <= int(choice) <= len(groups):
            group_name = list(groups.keys())[int(choice) - 1]
            tickers = groups[group_name]
        else:
            group_name = "Custom"
            tickers = [t.strip().upper() for t in choice.split(",") if t.strip()] or DEFAULT_TICKERS

        days_back = int(input("Enter analysis period (days, 1-10,000): ") or 100)

        run_pipeline(tickers, days_back, group_name=group_name)

    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
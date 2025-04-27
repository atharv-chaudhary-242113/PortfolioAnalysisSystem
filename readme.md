```markdown
# Portfolio Analysis System


A complete pipeline for fetching, analyzing, and visualizing global stock market data with IST timezone support.

## Features

- **Data Collection**: Fetch historical prices for stocks and indices from Yahoo Finance
- **Data Processing**: Clean and validate market data
- **Storage**: Save to CSV and MySQL database
- **Analysis**: Calculate returns, volatility, and risk metrics
- **Visualization**: Generate price charts and performance summaries
- **IST Support**: All timestamps in Asia/Kolkata timezone

## Pipeline Flow

1. **Scrape** market data from Yahoo Finance
2. **Clean** and validate the data
3. **Store** in CSV format
4. **Upload** to MySQL database
5. **Analyze** portfolio performance
6. **Visualize** results

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/portfolio-analysis.git
   cd portfolio-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MySQL database:
   ```sql
   CREATE DATABASE portfolio_db;
   ```

## Configuration

Edit the database credentials in `main.py`:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "portfolio_db"
}
```

## Usage

Run the main pipeline:
```bash
python main.py
```

### Command Line Interface

```
🕒 2025-04-06 18:30:45 IST
🚀 Starting Portfolio Analysis Pipeline

Supported Formats:
Indices: ^GSPC (S&P 500), ^IXIC (NASDAQ)
US Stocks: AAPL, TSLA
International: 7203.T (Toyota), HSBA.L (HSBC)

Enter symbols (comma separated) or press Enter for default: 
```

## File Structure

```
portfolio-analysis/
├── analysis/
│   └── portfolio_manager.py
├── database/
│   └── db_handler.py
├── scraper/
│   └── scraper.py
├── spreadsheets/
│   ├── csv_handler.py
│   └── data_cleaner.py
├── visuals/
│   └── visuals.py
├── main.py
├── README.md
└── requirements.txt
```

## Modules

1. **Scraper**: Fetches market data from Yahoo Finance
2. **Data Cleaner**: Validates and prepares data for analysis
3. **CSV Handler**: Manages CSV file operations
4. **DB Handler**: Handles MySQL database operations
5. **Portfolio Manager**: Calculates performance metrics
6. **Visuals**: Generates charts and tables

## Requirements

- Python 3.8+
- Packages:
  - yfinance
  - pandas
  - numpy
  - matplotlib
  - python-dotenv
  - mysql-connector-python
  - pytz
  - tabulate


```bash
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pytz
import matplotlib

matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import pandas as pd
from main import run_pipeline


class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Analysis System")
        self.root.geometry("900x700")
        self.style = ttk.Style()
        self.configure_styles()
        self.create_widgets()
        self.chart_windows = []

    def configure_styles(self):
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Console.TFrame', background='white')

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        ttk.Label(main_frame, text="Portfolio Analysis Dashboard",
                  style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)

        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Analysis Configuration", padding=10)
        config_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)

        # Ticker Selection
        ttk.Label(config_frame, text="Select Ticker Group:").grid(row=0, column=0, sticky=tk.W)
        self.group_var = tk.StringVar()
        groups = ["S&P 500 (Top 30)", "NASDAQ 100 (Top 30)", "Nifty 50 (India)",
                  "Global Blue Chips", "Custom"]
        self.group_combo = ttk.Combobox(config_frame, textvariable=self.group_var,
                                        values=groups, state="readonly", width=25)
        self.group_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.group_combo.current(0)

        # Custom Ticker Entry
        ttk.Label(config_frame, text="Custom Tickers (comma separated):").grid(row=1, column=0, sticky=tk.W)
        self.custom_entry = ttk.Entry(config_frame, width=40)
        self.custom_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.custom_entry.insert(0, "AAPL,MSFT,GOOGL")

        # Analysis Period
        ttk.Label(config_frame, text="Analysis Period (days):").grid(row=2, column=0, sticky=tk.W)
        self.days_var = tk.IntVar(value=100)
        ttk.Spinbox(config_frame, from_=1, to=365, textvariable=self.days_var,
                    width=5).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Output Console
        console_frame = ttk.LabelFrame(main_frame, text="Analysis Output", padding=10)
        console_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=5)

        self.console = tk.Text(console_frame, height=15, width=85, state='disabled',
                               font=('Consolas', 9), wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console['yscrollcommand'] = scrollbar.set

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Run Analysis", command=self.run_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Results", command=self.export_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Console", command=self.clear_console).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.cleanup).pack(side=tk.RIGHT, padx=5)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def run_analysis(self):
        group = self.group_var.get()
        custom_tickers = [t.strip().upper() for t in self.custom_entry.get().split(",") if t.strip()]
        days_back = self.days_var.get()

        if group == "Custom" and not custom_tickers:
            messagebox.showerror("Error", "Please enter custom tickers")
            return

        self.log_output(
            f"Starting analysis at {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_output(f"Parameters: Group={group}, Days={days_back}")

        try:
            if group == "Custom":
                tickers = custom_tickers
            else:
                from main import get_ticker_groups
                tickers = get_ticker_groups()[group]

            self.log_output("\nExecuting pipeline...")
            run_pipeline(tickers, days_back, self.log_output, self.root)
            self.log_output("\nAnalysis completed successfully!")

        except Exception as e:
            self.log_output(f"\nError: {str(e)}")
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")

    def export_results(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Analysis Results"
            )
            if file_path:
                # Add your export logic here
                messagebox.showinfo("Success", f"Results exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def clear_console(self):
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.config(state='disabled')

    def log_output(self, message):
        self.console.config(state='normal')
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')
        self.root.update()

    def cleanup(self):
        for window in self.chart_windows:
            try:
                window.destroy()
            except:
                pass
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()```
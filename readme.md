# Portfolio Analysis System

This is a Python-based desktop application for analyzing stock portfolios. It allows users to select predefined groups of stocks or enter custom tickers, specify a time period for analysis, and view basic portfolio statistics, correlations, and regression analysis. The application features a graphical user interface built with Tkinter.

## Features

* **Ticker Group Selection:** Choose from predefined groups of stocks (e.g., US Tech, Indian Finance) or enter a custom list of tickers.
* **Adjustable Analysis Period:** Specify the number of days to look back for historical stock data.
* **Real-time Data Fetching:** Uses the `yfinance` library to download up-to-date stock data.
* **Basic Portfolio Summary:** Provides key statistics for the selected portfolio.
* **Correlation Analysis:** Calculates and displays the correlation matrix between the price movements of the selected stocks.
* **Regression Analysis:** Performs linear regression of each stock's price against the first ticker in the selection to estimate Beta and Alpha.
* **Data Export:** Allows exporting the analysis results to a CSV file.
* **Report Options:** Provides a dialog to select which analysis components to include in the portfolio summary.
* **Clear Output Console:** Option to clear the analysis output displayed in the application.
* **Dark Theme:** Features a visually appealing dark theme for comfortable extended use.

## Prerequisites

Before running the application, ensure you have the following installed:

* **Python 3.9 or higher:** Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **Required Python Libraries:** Install these using pip:
    ```bash
    pip install yfinance pandas tkinter ttkthemes matplotlib scipy
    ```

## Installation

1.  **Clone the Repository (if you downloaded the code from GitHub):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
    Replace `<repository-url>` with the URL of the GitHub repository and `<repository-directory>` with the name of the cloned folder.

2.  **Navigate to the Project Directory (if you downloaded the code directly):**
    ```bash
    cd <project-directory>
    ```
    Replace `<project-directory>` with the path to the main project folder.

## Running the Application

To start the Portfolio Analysis System, run the `gui.py` file from your terminal:

```bash
python graphics/gui.py
````

This will launch the main application window.

## Usage

1.  **Select Ticker Group:** Use the dropdown menu to choose a predefined group of stocks or select "Custom".
2.  **Enter Custom Tickers (if "Custom" is selected):** In the "Custom Tickers" field, enter the stock tickers you want to analyze, separated by commas (e.g., AAPL,MSFT,GOOGL).
3.  **Specify Analysis Period:** Enter the number of days you want to analyze in the "Analysis Period (days)" field. You can also use the up and down arrow buttons to adjust the number of days.
4.  **Run Analysis:** Click the "Run Analysis" button to fetch the stock data and perform the initial analysis. The output will be displayed in the "Analysis Output" console.
5.  **Report Options:** Click the "Report Options" button to open a dialog where you can select which components (Basic Statistics, Correlation, Regression) you want to include in the portfolio summary.
6.  **Generate Summary:** After selecting the report options, click "Generate Summary" in the dialog to view the portfolio analysis based on your choices.
7.  **Export Results:** Click the "Export Results" button to save the raw analysis data to a CSV file. You will be prompted to choose a file name and location.
8.  **Clear Console:** Click the "Clear Console" button to clear the text in the "Analysis Output" area.
9.  **Exit:** Click the "Exit" button to close the application.

## Directory Structure

```
Python_CIA3c/
├── analysis/
│   └── portfolio_manager.py
├── assets/
│   └── themes/
│       └── forest-dark.tcl
├── graphics/
│   ├── buttons/
│   │   ├── export_results_button.py
│   │   └── report_options_button.py
│   ├── portfolio_summary/
│   │   └── portfolio_summary_generator.py
│   ├── report_options_dialog.py
│   └── gui.py
├── main.py
├── spreadsheets/
│   └── csv_handler.py
└── visuals/
    └── visuals.py
```

## Contributing

Contributions to this project are welcome. Feel free to fork the repository, make changes, and submit a pull request.

## License

[Specify your license here, e.g., MIT License, Apache 2.0, etc. If you don't have one yet, you can research open-source licenses and add one.]

---

**Enjoy analyzing your portfolios!**
```

This `README.md` file provides a good overview of your application, instructions on how to get it running, how to use its features, and a basic outline of the project structure. Remember to replace `[Specify your license here...]` with the actual license you choose for your project. You can save this content in a file named `README.md` in the root directory of your project. When you push your project to GitHub, this file will be automatically displayed on the repository's main page.
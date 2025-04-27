from tkinter import Toplevel, ttk
from tkinter import messagebox
from scipy.stats import linregress
from analysis.portfolio_manager import PortfolioManager  # Import your PortfolioManager

class PortfolioSummaryGenerator:
    def __init__(self, parent_app):
        self.parent_app = parent_app

    def generate_summary(self, data, options):
        if data is None or data.empty:
            self._show_summary_dialog("No data available for portfolio summary.")
            return

        # Assuming your cleaned_data DataFrame has 'Ticker', 'Date', 'Price' columns
        try:
            portfolio_manager = PortfolioManager(data.copy())
            summary_df = portfolio_manager.get_summary()
            summary_text = "Portfolio Summary:\n\n" + summary_df.to_string(index=False) + "\n\n"

            if "correlation" in options and len(data['Ticker'].unique()) > 1:
                # Basic correlation across all price series (can be expanded)
                price_data = data.pivot_table(index='Date', columns='Ticker', values='Price')
                if not price_data.empty:
                    correlation_matrix = price_data.corr()
                    summary_text += "Correlation Matrix:\n" + correlation_matrix.to_string() + "\n\n"
                else:
                    summary_text += "Correlation analysis not possible with current data.\n\n"

            if "regression" in options and len(data['Ticker'].unique()) > 1:
                first_ticker = data['Ticker'].unique()[0]
                summary_text += f"Regression Analysis (against {first_ticker}):\n"
                all_tickers = data['Ticker'].unique()[1:]
                price_data = data.pivot_table(index='Date', columns='Ticker', values='Price').dropna()
                if first_ticker in price_data.columns:
                    for ticker in all_tickers:
                        if ticker in price_data.columns:
                            y = price_data[ticker]
                            X = price_data[first_ticker]
                            if len(X) > 1:
                                slope, intercept, r_value, p_value, std_err = linregress(X, y)
                                summary_text += f"- {ticker}: Beta={slope:.4f}, Alpha={intercept:.4f}, R-squared={r_value**2:.4f}\n"
                            else:
                                summary_text += f"- {ticker}: Not enough data for regression.\n"
                    summary_text += "\n"
                else:
                    summary_text += f"Regression analysis not possible as '{first_ticker}' not found.\n\n"

            self._show_summary_dialog(summary_text)

        except ValueError as e:
            self._show_summary_dialog(f"Error generating summary: {e}")

    def _show_summary_dialog(self, summary_text):
        summary_dialog = Toplevel(self.parent_app.root)
        summary_dialog.title("Portfolio Summary")
        summary_frame = ttk.Frame(summary_dialog, padding=15)
        summary_frame.pack(fill="both", expand=True)
        summary_label = ttk.Label(summary_frame, text=summary_text, justify="left", font=('Consolas', 10)) # Use a monospaced font for better readability of tables
        summary_label.pack(fill="both", expand=True)
        close_button = ttk.Button(summary_frame, text="Close", command=summary_dialog.destroy)
        close_button.pack(pady=10)
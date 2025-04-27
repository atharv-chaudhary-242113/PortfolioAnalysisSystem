import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns  # For violin plot


class PortfolioVisuals:
    def __init__(self, portfolio_data, root=None):
        self.df = portfolio_data.copy()
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df.sort_values(['Ticker', 'Date'])
        self.root = root
        self.chart_options = {
            1: 'Line Chart',
            2: 'Histogram',
            3: 'Bar Graph',
            4: 'Box and Whiskers',
            5: 'Scatter Plot',
            6: 'Pie Chart',
            7: 'Area Chart',
            8: 'Violin Plot'
        }

    def plot_price_chart(self):
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        for ticker in self.df['Ticker'].unique():
            ticker_data = self.df[self.df['Ticker'] == ticker]
            ax.plot(ticker_data['Date'], ticker_data['Price'],
                    marker='o', markersize=4, linewidth=2, label=ticker)

        ax.set_title('Price Movement', pad=20, fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.7)

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Price Movement Chart")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_histogram(self):
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        all_prices = self.df['Price'].values
        ax.hist(all_prices, bins=20, edgecolor='black', alpha=0.7)
        ax.set_title('Price Distribution Across All Tickers', pad=20, fontsize=14)
        ax.set_xlabel('Price', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Price Histogram")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_bar_graph(self):
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        average_prices = self.df.groupby('Ticker')['Price'].mean()
        tickers = average_prices.index
        prices = average_prices.values
        ax.bar(tickers, prices, color='skyblue')
        ax.set_title('Average Price per Ticker', pad=20, fontsize=14)
        ax.set_xlabel('Ticker', fontsize=12)
        ax.set_ylabel('Average Price', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Average Price per Ticker")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_box_whisker(self):
        fig = Figure(figsize=(12, 7), dpi=100)
        ax = fig.add_subplot(111)
        tickers = self.df['Ticker'].unique()
        price_data = [self.df[self.df['Ticker'] == ticker]['Price'] for ticker in tickers]
        ax.boxplot(price_data, labels=tickers)
        ax.set_title('Price Distribution per Ticker', pad=20, fontsize=14)
        ax.set_xlabel('Ticker', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Price Distribution per Ticker (Box and Whiskers)")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_scatter_plot(self):
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Let's scatter plot Date vs. Price for the first ticker
        first_ticker = self.df['Ticker'].unique()[0]
        ticker_data = self.df[self.df['Ticker'] == first_ticker]
        ax.scatter(ticker_data['Date'], ticker_data['Price'], alpha=0.6)
        ax.set_title(f'Scatter Plot of Date vs. Price for {first_ticker}', pad=20, fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.autofmt_xdate()  # Rotate date labels for better readability

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title(f"Scatter Plot of Date vs. Price for {first_ticker}")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_pie_chart(self):
        fig = Figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)

        # Let's create a pie chart of the proportion of the last available price for each ticker
        last_prices = self.df.groupby('Ticker')['Price'].last()
        labels = last_prices.index
        sizes = last_prices.values

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Proportion of Last Available Price per Ticker', pad=20, fontsize=14)

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Proportion of Last Available Price per Ticker")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_area_chart(self):
        fig = Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)

        for ticker in self.df['Ticker'].unique():
            ticker_data = self.df[self.df['Ticker'] == ticker]
            ax.fill_between(ticker_data['Date'], ticker_data['Price'], alpha=0.4, label=ticker)
            ax.plot(ticker_data['Date'], ticker_data['Price'], linewidth=1) # Add line for better visibility

        ax.set_title('Price Movement (Area Chart)', pad=20, fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.autofmt_xdate()

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Price Movement (Area Chart)")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def plot_violin_plot(self):
        fig = Figure(figsize=(12, 7), dpi=100)
        ax = fig.add_subplot(111)

        sns.violinplot(x='Ticker', y='Price', data=self.df, ax=ax)
        ax.set_title('Price Distribution per Ticker (Violin Plot)', pad=20, fontsize=14)
        ax.set_xlabel('Ticker', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        if self.root:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Price Distribution per Ticker (Violin Plot)")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            toolbar_frame = tk.Frame(chart_window)
            toolbar_frame.pack(fill=tk.X)
            btn_close = tk.Button(toolbar_frame, text="Close", command=chart_window.destroy)
            btn_close.pack(side=tk.RIGHT, padx=5, pady=5)
        else:
            plt.show()

    def show_summary_table(self, pm_summary):
        formatted = pm_summary.copy()
        pct_cols = ['Return_Pct', 'Volatility_Pct', 'Best_Day_Pct', 'Worst_Day_Pct']

        for col in pct_cols:
            if col in formatted.columns:
                formatted[col] = formatted[col].apply(lambda x: f"{x}%")

        table = tabulate(formatted, headers='keys', tablefmt='grid', showindex=False)

        if self.root:
            table_window = tk.Toplevel(self.root)
            table_window.title("Performance Summary")
            text = tk.Text(table_window, font=('Consolas', 10), wrap=tk.NONE)
            text.insert(tk.END, table)
            text.config(state='disabled')
            scroll_x = tk.Scrollbar(table_window, orient=tk.HORIZONTAL, command=text.xview)
            scroll_y = tk.Scrollbar(table_window, orient=tk.VERTICAL, command=text.yview)
            text.configure(xscrollcommand=scroll_x.set, yscrollcommand=text.yview)
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            btn_close = tk.Button(table_window, text="Close", command=table_window.destroy)
            btn_close.pack(side=tk.BOTTOM, pady=5)
        else:
            print("\n" + " PORTFOLIO SUMMARY ".center(80, '='))
            print(table)
            print("=" * 80 + "\n")

    def plot_chart(self):
        self.chart_options = {
            1: 'Line Chart',
            2: 'Histogram',
            3: 'Bar Graph',
            4: 'Box and Whiskers',
            5: 'Scatter Plot',
            6: 'Pie Chart',
            7: 'Area Chart',
            8: 'Violin Plot'
        }
        options_text = "\nPlease select a chart type by number or name:\n"
        for number, name in self.chart_options.items():
            options_text += f"{number}) {name}\n"

        if self.root:
            chart_choice = simpledialog.askstring("Chart Type", options_text)
            if chart_choice:
                chart_choice = chart_choice.lower()
                selected_chart_name = None
                try:
                    choice_number = int(chart_choice)
                    if choice_number in self.chart_options:
                        selected_chart_name = self.chart_options[choice_number].lower().replace(" ", "")
                except ValueError:
                    selected_chart_name = chart_choice.lower().replace(" ", "")

                if selected_chart_name == 'linechart':
                    self.plot_price_chart()
                elif selected_chart_name == 'histogram':
                    self.plot_histogram()
                elif selected_chart_name == 'bargraph':
                    self.plot_bar_graph()
                elif selected_chart_name == 'boxandwhiskers':
                    self.plot_box_whisker()
                elif selected_chart_name == 'scatterplot':
                    self.plot_scatter_plot()
                elif selected_chart_name == 'piechart':
                    self.plot_pie_chart()
                elif selected_chart_name == 'areachart':
                    self.plot_area_chart()
                elif selected_chart_name == 'violinplot':
                    self.plot_violin_plot()
                else:
                    messagebox.showerror("Invalid Chart Type",
                                         f"Chart type '{chart_choice}' is not supported yet.")
        else:
            print(options_text)
            chart_choice = input("Enter your choice: ").lower()
            selected_chart_name = None
            try:
                choice_number = int(chart_choice)
                if choice_number in self.chart_options:
                    selected_chart_name = self.chart_options[choice_number].lower().replace(" ", "")
            except ValueError:
                selected_chart_name = chart_choice.lower().replace(" ", "")

            if selected_chart_name == 'linechart':
                self.plot_price_chart()
            elif selected_chart_name == 'histogram':
                self.plot_histogram()
            elif selected_chart_name == 'bargraph':
                self.plot_bar_graph()
            elif selected_chart_name == 'boxandwhiskers':
                self.plot_box_whisker()
            elif selected_chart_name == 'scatterplot':
                self.plot_scatter_plot()
            elif selected_chart_name == 'piechart':
                self.plot_pie_chart()
            elif selected_chart_name == 'areachart':
                self.plot_area_chart()
            elif selected_chart_name == 'violinplot':
                self.plot_violin_plot()
            else:
                print(f"Chart type '{chart_choice}' is not supported yet.")
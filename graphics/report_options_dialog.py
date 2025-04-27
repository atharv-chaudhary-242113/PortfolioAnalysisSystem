import tkinter as tk
from tkinter import ttk

class PortfolioAnalysisOptionsDialog(tk.Toplevel):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.title("Portfolio Analysis Options")
        self.parent = parent
        self.style = style
        self.options = {}
        self.result = None  # To store selected options
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Select analysis options:", style='TLabel').pack(pady=(0, 10))

        self.basic_stats_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Basic Statistics", variable=self.basic_stats_var, style='TCheckbutton').pack(anchor="w")
        self.options["basic_stats"] = self.basic_stats_var

        self.mean_returns_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Mean Returns (Annualized)", variable=self.mean_returns_var, style='TCheckbutton').pack(anchor="w")
        self.options["mean_returns"] = self.mean_returns_var

        self.volatility_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Volatility (Annualized)", variable=self.volatility_var, style='TCheckbutton').pack(anchor="w")
        self.options["volatility"] = self.volatility_var

        self.correlation_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Correlation Matrix", variable=self.correlation_var, style='TCheckbutton').pack(anchor="w")
        self.options["correlation"] = self.correlation_var

        self.regression_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Regression Analysis (vs. first ticker)", variable=self.regression_var, style='TCheckbutton').pack(anchor="w")
        self.options["regression"] = self.regression_var

        button_frame = ttk.Frame(main_frame, padding=(0, 15))
        button_frame.pack(fill="x")

        analyze_button = ttk.Button(button_frame, text="Generate Summary", command=self.analyze_portfolio, style='Accent.TButton')
        analyze_button.pack(side="left", padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right", padx=5)

        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def analyze_portfolio(self):
        selected_options = {key: var.get() for key, var in self.options.items() if var.get()}
        self.result = selected_options
        self.destroy()
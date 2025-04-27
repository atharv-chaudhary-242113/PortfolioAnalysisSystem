import tkinter as tk
import ctypes
if hasattr(ctypes, 'windll'):
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
from tkinter import ttk, messagebox, filedialog, Toplevel, Checkbutton
from datetime import datetime
import pytz
import matplotlib
import os
from scipy.stats import linregress

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from main import run_pipeline, get_ticker_groups
from spreadsheets.csv_handler import CSVHandler
from visuals.visuals import PortfolioVisuals  # Import PortfolioVisuals
from analysis.portfolio_manager import PortfolioManager  # Import your PortfolioManager
from graphics.report_options_dialog import PortfolioAnalysisOptionsDialog # Import the dialog
from graphics.buttons.report_options_button import ReportOptionsButtonHandler # Import Report Options handler
from graphics.buttons.export_results_button import ExportResultsButtonHandler # Import Export Results handler
from graphics.portfolio_summary.portfolio_summary_generator import PortfolioSummaryGenerator # Import the summary generator


class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Analysis System")
        self.root.geometry("950x750")  # Slightly larger default size

        # Configure dark theme styles
        self.style = ttk.Style()
        self.root.tk.call("source", "assets/themes/forest-dark.tcl")
        self.style.theme_use("forest-dark")

        # Enhanced style configurations
        self.style.configure('TFrame', padding=10)
        self.style.configure('TLabel', padding=(10, 7), font=('Arial', 11))
        self.style.configure('TButton', padding=(12, 9), font=('Arial', 11)) # Default button style
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), padding=(15, 15))
        self.style.configure('Section.TLabel', font=('Arial', 12, 'bold'), padding=(10, 10))
        self.style.configure('Highlight.TLabel', font=('Arial', 11, 'italic'), foreground="#aeea00", padding=(10, 7))
        self.style.configure('TEntry', padding=7, font=('Arial', 11))
        self.style.configure('TCombobox', padding=7, font=('Arial', 11))
        self.style.configure('TSpinbox', padding=7, font=('Arial', 11))
        self.style.configure('Console.TFrame', background="#282828", padding=8)
        self.style.configure('Console.TText', font=('Consolas', 10), foreground="#d3d3d3", background="#282828", insertbackground="#d3d3d3")
        self.style.configure('Vertical.TScrollbar', background="#383838", troughcolor="#202020")

        self.days_var = tk.IntVar(value=100)  # Initialize self.days_var here
        self.cleaned_data = None
        self.after_id = None  # To store the ID of the scheduled function
        self.repeat_delay = 500 # Initial delay in milliseconds
        self.acceleration_factor = 0.9 # Factor to reduce delay

        self.report_options_handler = ReportOptionsButtonHandler(self)
        self.export_results_handler = ExportResultsButtonHandler(self)
        self.summary_generator = PortfolioSummaryGenerator(self) # Create PortfolioSummaryGenerator instance
        self.create_widgets()
        self.chart_windows = []

    def _validate_days(self, new_value):
        if not new_value:
            return True
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    def _increment_days(self):
        try:
            current_days = self.days_var.get()
            self.days_var.set(current_days + 1)
        except tk.TclError:
            self.days_var.set(1) # Default if entry is invalid

    def _decrement_days(self):
        try:
            current_days = self.days_var.get()
            if current_days > 1:
                self.days_var.set(current_days - 1)
        except tk.TclError:
            self.days_var.set(1) # Default if entry is invalid

    def _start_increment(self, event):
        self.repeat_delay = 500
        self._repeat_increment()

    def _start_decrement(self, event):
        self.repeat_delay = 500
        self._repeat_decrement()

    def _repeat_increment(self):
        self._increment_days()
        self.repeat_delay = int(self.repeat_delay * self.acceleration_factor)
        if self.repeat_delay < 50: # Minimum delay
            self.repeat_delay = 50
        self.after_id = self.root.after(self.repeat_delay, self._repeat_increment)

    def _repeat_decrement(self):
        self._decrement_days()
        self.repeat_delay = int(self.repeat_delay * self.acceleration_factor)
        if self.repeat_delay < 50: # Minimum delay
            self.repeat_delay = 50
        self.after_id = self.root.after(self.repeat_delay, self._repeat_decrement)

    def _stop_repeat(self, event):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def clear_console(self):
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.config(state='disabled')

    def log_output(self, message, color=None, bold=False, highlight=False):
        self.console.config(state='normal')
        tag = ""
        if color:
            tag += f"color_{color}"
            self.console.tag_configure(tag, foreground=color)
        if bold:
            tag += "_bold"
            self.console.tag_configure(tag, font=('Consolas', 10, 'bold'))
        if highlight:
            tag += "_highlight"
            self.console.tag_configure(tag, background="#404040") # A slightly lighter dark background

        self.console.insert(tk.END, message + "\n", tag)
        self.console.see(tk.END)
        self.console.config(state='disabled')
        self.root.update()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(main_frame, text="Portfolio Analysis Dashboard", style='Header.TLabel')
        header_label.pack(pady=(10, 20), padx=20, fill="x")

        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Analysis Configuration", padding=15)
        config_frame.pack(pady=10, padx=20, fill="x")

        # Ticker Selection
        ttk.Label(config_frame, text="Select Ticker Group:", style='TLabel').grid(row=0, column=0, sticky="w", pady=5)
        self.group_var = tk.StringVar()
        groups = list(get_ticker_groups().keys()) + ["Custom"]
        self.group_combo = ttk.Combobox(config_frame, textvariable=self.group_var,
                                        values=groups, state="readonly", width=30, style='TCombobox')
        self.group_combo.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        self.group_combo.current(0)

        ttk.Label(config_frame, text="Custom Tickers (comma separated):", style='TLabel').grid(row=1, column=0, sticky="w", pady=5)
        self.custom_entry = ttk.Entry(config_frame, width=50, style='TEntry')
        self.custom_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        self.custom_entry.insert(0, "AAPL,MSFT,GOOGL")

        # Analysis Period (days) - Using a Frame for better layout
        days_label_frame = ttk.Frame(config_frame)
        days_label_frame.grid(row=2, column=0, sticky="w", pady=5)
        ttk.Label(days_label_frame, text="Analysis Period (days):", style='TLabel').pack(side=tk.LEFT)

        days_input_frame = ttk.Frame(config_frame)
        days_input_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.days_entry = ttk.Entry(days_input_frame, width=10, textvariable=self.days_var, style='TEntry', validate='key', validatecommand=(self.root.register(self._validate_days), '%P'))
        self.days_entry.pack(side=tk.LEFT)

        self.up_arrow_button = ttk.Button(days_input_frame, text="ᐃ", width=1, style='Accent.TButton', command=self._increment_days)
        self.up_arrow_button.pack(side=tk.LEFT, padx=(2, 0))
        self.up_arrow_button.bind('<ButtonPress-1>', self._start_increment)
        self.up_arrow_button.bind('<ButtonRelease-1>', self._stop_repeat)

        self.down_arrow_button = ttk.Button(days_input_frame, text="ᐁ", width=1, style='Accent.TButton', command=self._decrement_days)
        self.down_arrow_button.pack(side=tk.LEFT, padx=(2, 0))
        self.down_arrow_button.bind('<ButtonPress-1>', self._start_decrement)
        self.down_arrow_button.bind('<ButtonRelease-1>', self._stop_repeat)


        # Output Console
        console_label = ttk.Label(main_frame, text="Analysis Output", style='Section.TLabel')
        console_label.pack(pady=(20, 5), padx=20, fill="x")

        console_frame = ttk.Frame(main_frame, style='Console.TFrame')
        console_frame.pack(pady=5, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(console_frame, style="Vertical.TScrollbar") # Create scrollbar first
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.console = tk.Text(console_frame, height=15, width=90, state='disabled',
                               font=('Consolas', 10), wrap=tk.WORD,
                               background="#282828", foreground="#d3d3d3",
                               insertbackground="#d3d3d3",
                               yscrollcommand=scrollbar.set)  # Now scrollbar is defined
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar['command'] = self.console.yview # Link scrollbar command to text view

        # Buttons
        button_frame = ttk.Frame(main_frame, padding=15)
        button_frame.pack(pady=20, padx=20, fill="x")
        button_frame.config(width=500, height=80)
        button_frame.pack_propagate(False)

        run_button = ttk.Button(button_frame, text="Run Analysis", command=self.run_analysis, style='Accent.TButton')
        run_button.pack(side=tk.LEFT, padx=10)

        export_button = ttk.Button(button_frame, text="Export Results", command=self.export_results_handler.export_results, style='Accent.TButton')
        export_button.pack(side=tk.LEFT, padx=10)

        report_options_button = ttk.Button(button_frame, text="Report Options", command=self.report_options_handler.open_analysis_options, style='Accent.TButton')
        report_options_button.pack(side=tk.LEFT, padx=10)

        clear_button = ttk.Button(button_frame, text="Clear Console", command=self.clear_console, style='Accent.TButton')
        clear_button.pack(side=tk.LEFT, padx=10)

        exit_button = ttk.Button(button_frame, text="Exit", command=self.cleanup, style='Accent.TButton')
        exit_button.pack(side=tk.RIGHT, padx=10)

        # Configure grid weights for the configuration frame
        config_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def _open_analysis_options(self):
        if self.cleaned_data is None:
            messagebox.showerror("Error", "Please run the analysis first.")
            return
        dialog = PortfolioAnalysisOptionsDialog(self.root, self.style)
        if dialog.result:
            self.summary_generator.generate_summary(self.cleaned_data, dialog.result)

    def run_analysis(self):
        group = self.group_var.get()
        custom_tickers = [t.strip().upper() for t in self.custom_entry.get().split(",") if t.strip()]
        days_back = self.days_var.get()

        if group == "Custom" and not custom_tickers:
            messagebox.showerror("Error", "Please enter custom tickers")
            return

        self.log_output(
            f"Starting analysis for group: {group} at {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}",
            highlight=True
        )

        try:
            if group == "Custom":
                tickers = custom_tickers
            else:
                tickers = get_ticker_groups()[group]

            self.log_output("\nExecuting pipeline...", highlight=True)
            cleaned_data = run_pipeline(tickers, days_back, self.log_output, self.root, group)
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data
                self.log_output("\nAnalysis completed successfully!", highlight=True)
            else:
                self.log_output("\nAnalysis completed with warnings", highlight=True)

        except Exception as e:
            error_message = f"\nError: {str(e)}"
            self.log_output(error_message, color="red", bold=True)
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")

    def generate_chart(self):
        if self.cleaned_data is None:
            messagebox.showerror("Error", "Please run the analysis first to generate charts.")
            return

        visualizer = PortfolioVisuals(self.cleaned_data, self.root)
        visualizer.plot_chart()

    def clear_console(self):
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.config(state='disabled')

    def log_output(self, message, color=None, bold=False, highlight=False):
        self.console.config(state='normal')
        tag = ""
        if color:
            tag += f"color_{color}"
            self.console.tag_configure(tag, foreground=color)
        if bold:
            tag += "_bold"
            self.console.tag_configure(tag, font=('Consolas', 10, 'bold'))
        if highlight:
            tag += "_highlight"
            self.console.tag_configure(tag, background="#404040") # A slightly lighter dark background

        self.console.insert(tk.END, message + "\n", tag)
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
    root.mainloop()
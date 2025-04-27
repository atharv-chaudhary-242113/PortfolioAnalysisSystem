from tkinter import messagebox, filedialog
import os
from datetime import datetime
from spreadsheets.csv_handler import CSVHandler

class ExportResultsButtonHandler:
    def __init__(self, parent_app):
        self.parent_app = parent_app

    def export_results(self):
        if self.parent_app.cleaned_data is None:
            messagebox.showerror("Error", "No analysis results available to export.")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Analysis Results",
                initialfile=f"portfolio_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if file_path:
                csv_handler = CSVHandler()
                csv_handler.save_to_csv(self.parent_app.cleaned_data, os.path.basename(file_path))
                messagebox.showinfo("Success", f"Results exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
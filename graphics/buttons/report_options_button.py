# graphics/buttons/report_options_button.py
from tkinter import messagebox
from graphics.report_options_dialog import PortfolioAnalysisOptionsDialog

class ReportOptionsButtonHandler:
    def __init__(self, parent_app):
        self.parent_app = parent_app

    def open_analysis_options(self):
        if self.parent_app.cleaned_data is None:
            messagebox.showerror("Error", "Please run the analysis first.")
            return
        dialog = PortfolioAnalysisOptionsDialog(self.parent_app.root, self.parent_app.style)
        if dialog.result:
            self.parent_app.summary_generator.generate_summary(self.parent_app.cleaned_data, dialog.result)
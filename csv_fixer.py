import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, Frame, messagebox
import os

class CSVFixer:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Fixer")
        self.root.geometry("800x600")

        self.frame = Frame(root)
        self.frame.pack(pady=20)

        self.label = Label(self.frame, text="Upload a CSV file to format and clean", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.upload_button = Button(self.frame, text="Upload CSV", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.process_button = Button(self.frame, text="Process File", command=self.process_file, state='disabled')
        self.process_button.pack(pady=10)

        self.save_button = Button(self.frame, text="Save Processed File", command=self.save_file, state='disabled')
        self.save_button.pack(pady=10)

        self.status_label = Label(root, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.data = None
        self.processed_data = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.status_label.config(text="File uploaded successfully.")
                self.process_button.config(state='normal')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.data = None

    def process_file(self):
        if self.data is not None:
            try:
                self.processed_data = self.data.copy()
                self.processed_data.fillna(self.processed_data.mean(), inplace=True)

                num_cols = self.processed_data.select_dtypes(include=[np.number]).columns
                self.processed_data[num_cols] = (self.processed_data[num_cols] - self.processed_data[num_cols].min()) / (self.processed_data[num_cols].max() - self.processed_data[num_cols].min())

                cat_cols = self.processed_data.select_dtypes(include=[object]).columns
                for col in cat_cols:
                    self.processed_data[col] = self.processed_data[col].astype('category').cat.codes
                self.generate_summary_report()

                self.status_label.config(text="File processed successfully.")
                self.save_button.config(state='normal')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process file: {str(e)}")

    def save_file(self):
        if self.processed_data is not None:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if save_path:
                try:
                    self.processed_data.to_csv(save_path, index=False)
                    messagebox.showinfo("Saved", f"Processed file saved at {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def generate_summary_report(self):
        if self.processed_data is not None:
            plt.figure(figsize=(10, 6))

            num_cols = self.processed_data.select_dtypes(include=[np.number]).columns
            self.processed_data[num_cols].hist(bins=15, figsize=(15, 6), layout=(2, 4))

            plt.tight_layout()
            report_path = os.path.join(os.getcwd(), 'summary_report.png')
            try:
                plt.savefig(report_path)
                plt.close()
                messagebox.showinfo("Summary Report", f"Summary report generated at {report_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate summary report: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = CSVFixer(root)
    root.mainloop()
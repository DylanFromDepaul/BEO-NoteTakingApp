import tkinter as tk
from tkinter import ttk

class PreviewView(ttk.Frame):
    """
    Displays the formatted BEO notes.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.text_preview = tk.Text(self, wrap='word')
        self.text_preview.pack(fill=tk.BOTH, expand=True)
        self.text_preview.config(state=tk.DISABLED)

    def update_preview(self, formatted_text):
        self.text_preview.config(state=tk.NORMAL)
        self.text_preview.delete(1.0, tk.END)
        self.text_preview.insert(tk.END, formatted_text)
        self.text_preview.config(state=tk.DISABLED)

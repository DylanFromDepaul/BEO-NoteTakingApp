import tkinter as tk
from tkinter import ttk, messagebox

class EquipmentView(ttk.Frame):
    """
    Manages equipment-related UI components.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.bind_callbacks()

    def create_widgets(self):
        equipment_frame = ttk.LabelFrame(self, text="Equipment Management")
        equipment_frame.pack(fill=tk.X, padx=10, pady=5)

        equipment_frame.columnconfigure(1, weight=1)

        # Equipment Entry
        ttk.Label(equipment_frame, text="Equipment:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.equipment_entry = ttk.Entry(equipment_frame)
        self.equipment_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        # Notes Entry
        ttk.Label(equipment_frame, text="Notes:").grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self.notes_entry = tk.Text(equipment_frame, height=3)
        self.notes_entry.grid(row=1, column=1, sticky='we', padx=5, pady=5)

        # Add and Remove Buttons
        button_frame = ttk.Frame(equipment_frame)
        button_frame.grid(row=2, column=1, sticky='e', padx=5, pady=5)
        self.add_notes_button = ttk.Button(button_frame, text="Add Notes", command=self.on_add_notes)
        self.add_notes_button.pack(side=tk.LEFT, padx=5)
        self.remove_notes_button = ttk.Button(button_frame, text="Remove Notes", command=self.on_remove_notes)
        self.remove_notes_button.pack(side=tk.LEFT)

    def bind_callbacks(self):
        self.on_add_notes_callback = None
        self.on_remove_notes_callback = None

    def set_on_add_notes_callback(self, callback):
        self.on_add_notes_callback = callback

    def set_on_remove_notes_callback(self, callback):
        self.on_remove_notes_callback = callback

    def get_equipment(self):
        return self.equipment_entry.get().strip()

    def get_notes(self):
        return self.notes_entry.get("1.0", tk.END).strip()

    def clear_entries(self):
        self.equipment_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

    def on_add_notes(self):
        if self.on_add_notes_callback:
            self.on_add_notes_callback()
        else:
            messagebox.showerror("Action Error", "No action bound for adding notes.")

    def on_remove_notes(self):
        if self.on_remove_notes_callback:
            self.on_remove_notes_callback()
        else:
            messagebox.showerror("Action Error", "No action bound for removing notes.")

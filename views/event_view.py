import tkinter as tk
from tkinter import ttk, messagebox

class EventView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.on_event_select_callback = None

    def create_widgets(self):
        event_frame = self

        event_frame.columnconfigure(1, weight=1)

        # Event Name
        ttk.Label(event_frame, text="Event Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.event_name_entry = ttk.Entry(event_frame)
        self.event_name_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        # Start Time
        ttk.Label(event_frame, text="Start Time:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.event_start_time_entry = ttk.Entry(event_frame)
        self.event_start_time_entry.grid(row=1, column=1, sticky='we', padx=5, pady=5)

        # End Time
        ttk.Label(event_frame, text="End Time:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.event_end_time_entry = ttk.Entry(event_frame)
        self.event_end_time_entry.grid(row=2, column=1, sticky='we', padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(event_frame)
        button_frame.grid(row=3, column=1, sticky='e', padx=5, pady=5)
        add_event_button = ttk.Button(button_frame, text="Add Event", command=self.on_add_event)
        add_event_button.pack(side=tk.LEFT, padx=5)
        remove_event_button = ttk.Button(button_frame, text="Remove Event", command=self.on_remove_event)
        remove_event_button.pack(side=tk.LEFT)

        # Event List (Optional)
        self.event_listbox = tk.Listbox(event_frame)
        self.event_listbox.grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=5)
        self.event_listbox.bind("<<ListboxSelect>>", self.on_event_select)

    def bind_event_select(self, callback):
        self.on_event_select_callback = callback

    def on_event_select(self, event):
        selection = self.event_listbox.curselection()
        if not selection:
            return
        selected_event_name = self.event_listbox.get(selection[0])
        if self.on_event_select_callback:
            self.on_event_select_callback(selected_event_name)

    # Implement on_add_event and on_remove_event methods as appropriate
    def on_add_event(self):
        # Add event logic
        pass

    def on_remove_event(self):
        # Remove event logic
        pass

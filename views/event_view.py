import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class EventView(tk.Frame):
    """
    Manages event-related UI components.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='nsew')  # Use grid geometry manager

        # Initialize callbacks
        self.on_add_event_callback = None
        self.on_remove_event_callback = None
        self.on_update_event_callback = None
        self.on_get_event_callback = None

        # State to track if we are editing an event
        self.editing_event = False
        self.current_event_name = None

        self.selected_group_name = None  # Store the selected group name

        # Configure grid weights for resizing
        self.columnconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        # Event Name
        tk.Label(self, text="Event Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.event_name_entry = tk.Entry(self)
        self.event_name_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        # Start Time
        tk.Label(self, text="Start Time:").grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        start_time_frame = tk.Frame(self)
        start_time_frame.grid(row=1, column=1, sticky='w')

        # Hour Dropdown
        tk.Label(start_time_frame, text="Hour:").grid(row=0, column=0, padx=2)
        self.start_hour_var = tk.StringVar(value="1")
        self.start_hour_menu = ttk.Combobox(
            start_time_frame,
            textvariable=self.start_hour_var,
            values=[str(i) for i in range(1, 13)],
            width=3,
            state="readonly"
        )
        self.start_hour_menu.grid(row=0, column=1, padx=2)

        # Minute Dropdown
        tk.Label(start_time_frame, text="Minute:").grid(row=0, column=2, padx=2)
        self.start_minute_var = tk.StringVar(value="00")
        self.start_minute_menu = ttk.Combobox(
            start_time_frame,
            textvariable=self.start_minute_var,
            values=["00", "15", "30", "45"],
            width=3,
            state="readonly"
        )
        self.start_minute_menu.grid(row=0, column=3, padx=2)

        # AM/PM Dropdown
        tk.Label(start_time_frame, text="AM/PM:").grid(row=0, column=4, padx=2)
        self.start_am_pm_var = tk.StringVar(value="AM")
        self.start_am_pm_menu = ttk.Combobox(
            start_time_frame,
            textvariable=self.start_am_pm_var,
            values=["AM", "PM"],
            width=3,
            state="readonly"
        )
        self.start_am_pm_menu.grid(row=0, column=5, padx=2)

        # End Time (Optional)
        tk.Label(self, text="End Time (Optional):").grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        end_time_frame = tk.Frame(self)
        end_time_frame.grid(row=2, column=1, sticky='w')

        # Hour Dropdown
        tk.Label(end_time_frame, text="Hour:").grid(row=0, column=0, padx=2)
        self.end_hour_var = tk.StringVar(value="")
        self.end_hour_menu = ttk.Combobox(
            end_time_frame,
            textvariable=self.end_hour_var,
            values=[str(i) for i in range(1, 13)],
            width=3,
            state="readonly"
        )
        self.end_hour_menu.grid(row=0, column=1, padx=2)

        # Minute Dropdown
        tk.Label(end_time_frame, text="Minute:").grid(row=0, column=2, padx=2)
        self.end_minute_var = tk.StringVar(value="")
        self.end_minute_menu = ttk.Combobox(
            end_time_frame,
            textvariable=self.end_minute_var,
            values=["00", "15", "30", "45"],
            width=3,
            state="readonly"
        )
        self.end_minute_menu.grid(row=0, column=3, padx=2)

        # AM/PM Dropdown
        tk.Label(end_time_frame, text="AM/PM:").grid(row=0, column=4, padx=2)
        self.end_am_pm_var = tk.StringVar(value="")
        self.end_am_pm_menu = ttk.Combobox(
            end_time_frame,
            textvariable=self.end_am_pm_var,
            values=["AM", "PM"],
            width=3,
            state="readonly"
        )
        self.end_am_pm_menu.grid(row=0, column=5, padx=2)

        # Location
        tk.Label(self, text="Location (Optional):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.location_entry = tk.Entry(self)
        self.location_entry.grid(row=3, column=1, sticky='we', padx=5, pady=5)

        # Equipment
        tk.Label(self, text="Equipment (Optional):").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.equipment_entry = tk.Entry(self)
        self.equipment_entry.grid(row=4, column=1, sticky='we', padx=5, pady=5)

        # Notes
        tk.Label(self, text="Notes (Optional):").grid(row=5, column=0, sticky='ne', padx=5, pady=5)
        self.notes_entry = tk.Entry(self)
        self.notes_entry.grid(row=5, column=1, sticky='we', padx=5, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Add Event Button
        self.add_event_button = tk.Button(button_frame, text="Add Event", command=self.on_add_event)
        self.add_event_button.pack(side='left', padx=5)

        # Edit Event Button
        self.edit_event_button = tk.Button(button_frame, text="Edit Event", command=self.on_edit_event)
        self.edit_event_button.pack(side='left', padx=5)

        # Remove Event Button
        self.remove_event_button = tk.Button(button_frame, text="Remove Event", command=self.on_remove_event)
        self.remove_event_button.pack(side='left', padx=5)

        # Event List
        tk.Label(self, text="Events:").grid(row=7, column=0, sticky='ne', padx=5, pady=5)
        self.event_listbox = tk.Listbox(self)
        self.event_listbox.grid(row=7, column=1, sticky='nsew', padx=5, pady=5)
        self.event_listbox.bind('<<ListboxSelect>>', self.on_event_select)

        # Configure row and column weights for the listbox to expand
        self.rowconfigure(7, weight=1)
        self.columnconfigure(1, weight=1)

    def on_add_event(self):
        event_name = self.event_name_entry.get()

        # Construct Start Time
        start_hour = self.start_hour_var.get()
        start_minute = self.start_minute_var.get()
        start_am_pm = self.start_am_pm_var.get()
        if not start_hour or not start_minute or not start_am_pm:
            messagebox.showerror("Input Error", "Please select a valid start time.")
            return
        start_time = f"{start_hour}:{start_minute} {start_am_pm}"

        # Construct End Time
        end_time = ""
        end_hour = self.end_hour_var.get()
        end_minute = self.end_minute_var.get()
        end_am_pm = self.end_am_pm_var.get()
        if end_hour and end_minute and end_am_pm:
            end_time = f"{end_hour}:{end_minute} {end_am_pm}"

        location = self.location_entry.get()
        equipment = self.equipment_entry.get()
        notes = self.notes_entry.get()

        if not event_name:
            messagebox.showerror("Input Error", "Please enter at least an event name.")
            return

        if not self.selected_group_name:
            messagebox.showerror("Group Selection Error", "No group selected. Please select a group.")
            return

        event_data = {
            'event_name': event_name,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'equipment': equipment,
            'notes': notes,
            'group_name': self.selected_group_name,
            'original_event_name': self.current_event_name,
        }

        success = False
        if self.editing_event and self.on_update_event_callback:
            success = self.on_update_event_callback(event_data)
            if success:
                self.add_event_button.config(text="Add Event")
                self.editing_event = False
                self.current_event_name = None
        elif self.on_add_event_callback:
            success = self.on_add_event_callback(event_data)
        else:
            messagebox.showerror("Action Error", "No action bound for adding/updating events.")

        if success:
            self.clear_event_entries()
            self.update_event_list()  # Refresh the event list after adding

    def on_edit_event(self):
        # Implement the logic for editing an event
        pass  # To be implemented as per your application logic

    def on_remove_event(self):
        selected_event = self.event_listbox.get(tk.ACTIVE)
        if not selected_event:
            messagebox.showerror("Selection Error", "No event selected. Please select an event to remove.")
            return

        if not self.selected_group_name:
            messagebox.showerror("Group Selection Error", "No group selected.")
            return

        if self.on_remove_event_callback:
            success = self.on_remove_event_callback(self.selected_group_name, selected_event)
            if success:
                self.update_event_list()  # Refresh the event list after removal
        else:
            messagebox.showerror("Action Error", "No action bound for removing events.")

    def on_event_select(self, event):
        selection = self.event_listbox.curselection()
        if not selection:
            return
        selected_event = self.event_listbox.get(selection[0])

        if not self.selected_group_name:
            return

        if self.on_get_event_callback:
            event_data = self.on_get_event_callback(self.selected_group_name, selected_event)
            if event_data:
                self.populate_event_entries(event_data)
                self.editing_event = True
                self.current_event_name = event_data['event_name']
                self.add_event_button.config(text="Update Event")

    def populate_event_entries(self, event_data):
        self.event_name_entry.delete(0, tk.END)
        self.event_name_entry.insert(0, event_data['event_name'])

        # Parse Start Time
        start_time = event_data['start_time']
        if start_time:
            try:
                start_hour_minute, start_am_pm = start_time.strip().split()
                start_hour, start_minute = start_hour_minute.strip().split(':')
                self.start_hour_var.set(start_hour)
                self.start_minute_var.set(start_minute)
                self.start_am_pm_var.set(start_am_pm)
            except ValueError:
                pass  # Handle parsing errors if necessary

        # Parse End Time if it exists
        end_time = event_data.get('end_time', '')
        if end_time:
            try:
                end_hour_minute, end_am_pm = end_time.strip().split()
                end_hour, end_minute = end_hour_minute.strip().split(':')
                self.end_hour_var.set(end_hour)
                self.end_minute_var.set(end_minute)
                self.end_am_pm_var.set(end_am_pm)
            except ValueError:
                pass

        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, event_data.get('location', ''))

        self.equipment_entry.delete(0, tk.END)
        self.equipment_entry.insert(0, event_data.get('equipment', ''))

        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, event_data.get('notes', ''))

    def clear_event_entries(self):
        self.event_name_entry.delete(0, tk.END)

        self.start_hour_var.set("1")
        self.start_minute_var.set("00")
        self.start_am_pm_var.set("AM")

        self.end_hour_var.set("")
        self.end_minute_var.set("")
        self.end_am_pm_var.set("")

        self.location_entry.delete(0, tk.END)
        self.equipment_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        self.add_event_button.config(text="Add Event")
        self.editing_event = False
        self.current_event_name = None

    def set_selected_group(self, group_name):
        self.selected_group_name = group_name

    def bind_add_event(self, callback):
        self.on_add_event_callback = callback

    def bind_remove_event(self, callback):
        self.on_remove_event_callback = callback

    def bind_update_event(self, callback):
        self.on_update_event_callback = callback

    def bind_get_event(self, callback):
        self.on_get_event_callback = callback

    def update_event_list(self, events=None):
        self.event_listbox.delete(0, tk.END)
        if self.on_get_event_callback and self.selected_group_name:
            group_events = self.on_get_event_callback(self.selected_group_name)
            if group_events:
                for event_name in group_events:
                    self.event_listbox.insert(tk.END, event_name)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Event Manager")
    root.geometry("600x400")

    event_view = EventView(master=root)
    root.mainloop()

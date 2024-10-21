import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from views.preview_view import PreviewView
from views.equipment_view import EquipmentView
from views.event_view import EventView


class MainView(tk.Tk):
    """
    The main UI for the BEO Note-Taking Application.
    """

    def __init__(self):
        super().__init__()
        self.title("BEO Note-Taking Application")
        self.controller = None
        self.current_date_str = None
        self.current_group_name = None
        self.current_meeting_name = None
        self.current_event_name = None
        self.editing_event = False
        self.create_widgets()

    def set_controller(self, controller):
        self.controller = controller
        self.refresh_tree()
        self.generate_text()

    def create_widgets(self):
        # Configure main window to be resizable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)  # Treeview frame
        self.rowconfigure(1, weight=1)  # Bottom frame with forms and preview

        # Style configuration
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=10)

        # Top frame for the Treeview
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=0, column=0, sticky='nsew')

        # Bottom frame for forms and preview
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, sticky='nsew')

        # Configure grid weights for frames
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        # Create the Treeview widget in tree_frame
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add a vertical scrollbar to the Treeview
        tree_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        tree_scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=tree_scrollbar.set)

        # Define columns
        self.tree['columns'] = ('Details',)
        self.tree.column('#0', anchor='w', stretch=True)
        self.tree.column('Details', anchor='w', stretch=True)
        self.tree.heading('#0', text='Date/Group/Meeting/Event')
        self.tree.heading('Details', text='Details')

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Create notebook in bottom_frame
        self.notebook = ttk.Notebook(self.bottom_frame)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Configure bottom_frame to expand
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        # Create frames for notebook tabs
        self.forms_frame = ttk.Frame(self.notebook)
        self.preview_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.forms_frame, text='Forms')
        self.notebook.add(self.preview_frame, text='Preview')

        # Configure frames to expand
        self.forms_frame.columnconfigure(0, weight=1)
        self.forms_frame.rowconfigure(0, weight=1)
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)

        # Create form sections in forms_frame
        self.create_date_management(self.forms_frame)
        self.create_group_management(self.forms_frame)
        self.create_meeting_management(self.forms_frame)
        self.create_event_form(self.forms_frame)
        self.create_equipment_management(self.forms_frame)

        # Preview View
        self.preview_view = PreviewView(self.preview_frame)
        self.preview_view.pack(fill=tk.BOTH, expand=True)

    def create_date_management(self, parent):
        date_frame = ttk.LabelFrame(parent, text="Date Management")
        date_frame.pack(fill=tk.X, padx=10, pady=5)

        date_frame.columnconfigure(1, weight=1)

        ttk.Label(date_frame, text="Date:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = ttk.Entry(date_frame)
        self.date_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        add_date_button = ttk.Button(date_frame, text="Add Date", command=self.on_add_date)
        add_date_button.grid(row=0, column=2, padx=5, pady=5)

        remove_date_button = ttk.Button(date_frame, text="Remove Date", command=self.on_remove_date)
        remove_date_button.grid(row=0, column=3, padx=5, pady=5)

    def create_group_management(self, parent):
        group_frame = ttk.LabelFrame(parent, text="Group Management")
        group_frame.pack(fill=tk.X, padx=10, pady=5)

        group_frame.columnconfigure(1, weight=1)

        ttk.Label(group_frame, text="Group Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.group_name_entry = ttk.Entry(group_frame)
        self.group_name_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        add_group_button = ttk.Button(group_frame, text="Add Group", command=self.on_add_group)
        add_group_button.grid(row=0, column=2, padx=5, pady=5)

        remove_group_button = ttk.Button(group_frame, text="Remove Group", command=self.on_remove_group)
        remove_group_button.grid(row=0, column=3, padx=5, pady=5)

    def create_meeting_management(self, parent):
        meeting_frame = ttk.LabelFrame(parent, text="Meeting Management")
        meeting_frame.pack(fill=tk.X, padx=10, pady=5)

        meeting_frame.columnconfigure(1, weight=1)
        meeting_frame.columnconfigure(3, weight=1)

        ttk.Label(meeting_frame, text="Meeting Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.meeting_name_entry = ttk.Entry(meeting_frame)
        self.meeting_name_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        ttk.Label(meeting_frame, text="Location:").grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.meeting_location_entry = ttk.Entry(meeting_frame)
        self.meeting_location_entry.grid(row=0, column=3, sticky='we', padx=5, pady=5)

        add_meeting_button = ttk.Button(meeting_frame, text="Add Meeting", command=self.on_add_meeting)
        add_meeting_button.grid(row=0, column=4, padx=5, pady=5)

        remove_meeting_button = ttk.Button(meeting_frame, text="Remove Meeting", command=self.on_remove_meeting)
        remove_meeting_button.grid(row=1, column=4, padx=5, pady=5)

    def create_event_form(self, parent):
        event_frame = ttk.LabelFrame(parent, text="Event Management")
        event_frame.pack(fill=tk.X, padx=10, pady=5)

        event_frame.columnconfigure(1, weight=1)

        # Event Name
        ttk.Label(event_frame, text="Event Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.event_name_entry = ttk.Entry(event_frame)
        self.event_name_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)

        # Start Time
        ttk.Label(event_frame, text="Start Time:").grid(row=1, column=0, sticky='e', padx=5, pady=5)

        start_time_frame = ttk.Frame(event_frame)
        start_time_frame.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        start_hours = [str(h).zfill(2) for h in range(1, 13)]
        start_minutes = [str(m).zfill(2) for m in range(0, 60, 5)]
        start_am_pm = ['AM', 'PM']

        self.start_hour_var = tk.StringVar(value='01')
        self.start_minute_var = tk.StringVar(value='00')
        self.start_am_pm_var = tk.StringVar(value='AM')

        ttk.OptionMenu(start_time_frame, self.start_hour_var, self.start_hour_var.get(), *start_hours).pack(side=tk.LEFT)
        ttk.Label(start_time_frame, text=":").pack(side=tk.LEFT)
        ttk.OptionMenu(start_time_frame, self.start_minute_var, self.start_minute_var.get(), *start_minutes).pack(side=tk.LEFT)
        ttk.OptionMenu(start_time_frame, self.start_am_pm_var, self.start_am_pm_var.get(), *start_am_pm).pack(side=tk.LEFT)

        # End Time
        ttk.Label(event_frame, text="End Time:").grid(row=2, column=0, sticky='e', padx=5, pady=5)

        end_time_frame = ttk.Frame(event_frame)
        end_time_frame.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        end_hours = [str(h).zfill(2) for h in range(1, 13)]
        end_minutes = [str(m).zfill(2) for m in range(0, 60, 5)]
        end_am_pm = ['AM', 'PM']

        self.end_hour_var = tk.StringVar(value='01')
        self.end_minute_var = tk.StringVar(value='00')
        self.end_am_pm_var = tk.StringVar(value='AM')

        ttk.OptionMenu(end_time_frame, self.end_hour_var, self.end_hour_var.get(), *end_hours).pack(side=tk.LEFT)
        ttk.Label(end_time_frame, text=":").pack(side=tk.LEFT)
        ttk.OptionMenu(end_time_frame, self.end_minute_var, self.end_minute_var.get(), *end_minutes).pack(side=tk.LEFT)
        ttk.OptionMenu(end_time_frame, self.end_am_pm_var, self.end_am_pm_var.get(), *end_am_pm).pack(side=tk.LEFT)

        # Buttons
        button_frame = ttk.Frame(event_frame)
        button_frame.grid(row=3, column=1, sticky='e', padx=5, pady=5)
        add_event_button = ttk.Button(button_frame, text="Add Event", command=self.on_add_event)
        add_event_button.pack(side=tk.LEFT, padx=5)
        remove_event_button = ttk.Button(button_frame, text="Remove Event", command=self.on_remove_event)
        remove_event_button.pack(side=tk.LEFT)

    def on_event_select(self, selected_event_name):
        self.current_event_name = selected_event_name
        date_str = self.current_date_str
        group_name = self.current_group_name
        meeting_name = self.current_meeting_name

        if not date_str or not group_name or not meeting_name:
            return

        event_data = self.controller.get_event(date_str, group_name, meeting_name, selected_event_name)
        if event_data:
            # Populate event fields
            self.event_name_entry.delete(0, tk.END)
            self.event_name_entry.insert(0, event_data['event_name'])
            self.event_start_time_entry.delete(0, tk.END)
            self.event_start_time_entry.insert(0, event_data['start_time'])
            self.event_end_time_entry.delete(0, tk.END)
            self.event_end_time_entry.insert(0, event_data['end_time'])

            # Populate equipment and notes
            self.equipment_view.equipment_entry.delete(0, tk.END)
            self.equipment_view.equipment_entry.insert(0, event_data.get('equipment', ''))
            self.equipment_view.notes_entry.delete("1.0", tk.END)
            self.equipment_view.notes_entry.insert("1.0", event_data.get('notes', ''))

    def create_equipment_management(self, parent):
        equipment_frame = ttk.LabelFrame(parent, text="Equipment Management")
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
        add_notes_button = ttk.Button(button_frame, text="Add Notes", command=self.on_add_notes)
        add_notes_button.pack(side=tk.LEFT, padx=5)
        remove_notes_button = ttk.Button(button_frame, text="Remove Notes", command=self.on_remove_notes)
        remove_notes_button.pack(side=tk.LEFT)

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        item_text = self.tree.item(selected_item, 'text')
        item_tags = self.tree.item(selected_item, 'tags')

        if 'date' in item_tags:
            self.current_date_str = item_text
            self.current_group_name = None
            self.current_meeting_name = None
            self.current_event_name = None
            self.clear_equipment_entries()
        elif 'group' in item_tags:
            self.current_group_name = item_text
            parent_item = self.tree.parent(selected_item)
            self.current_date_str = self.tree.item(parent_item, 'text')
            self.current_meeting_name = None
            self.current_event_name = None
            self.clear_equipment_entries()
        elif 'meeting' in item_tags:
            self.current_meeting_name = item_text
            parent_item = self.tree.parent(selected_item)
            self.current_group_name = self.tree.item(parent_item, 'text')
            grandparent_item = self.tree.parent(parent_item)
            self.current_date_str = self.tree.item(grandparent_item, 'text')
            self.current_event_name = None

            # Populate equipment and notes for the selected meeting
            meeting_data = self.controller.get_meeting(self.current_date_str, self.current_group_name, self.current_meeting_name)
            if meeting_data:
                self.equipment_entry.delete(0, tk.END)
                self.equipment_entry.insert(0, meeting_data.get('equipment', ''))
                self.notes_entry.delete("1.0", tk.END)
                self.notes_entry.insert("1.0", meeting_data.get('notes', ''))
        elif 'event' in item_tags:
            self.current_event_name = item_text
            parent_item = self.tree.parent(selected_item)
            self.current_meeting_name = self.tree.item(parent_item, 'text')
            grandparent_item = self.tree.parent(parent_item)
            self.current_group_name = self.tree.item(grandparent_item, 'text')
            great_grandparent_item = self.tree.parent(grandparent_item)
            self.current_date_str = self.tree.item(great_grandparent_item, 'text')

    def on_add_date(self):
        date_str = self.date_entry.get().strip()
        if not date_str:
            messagebox.showerror("Input Error", "Date cannot be empty.")
            return
        success = self.controller.add_date(date_str)
        if success:
            self.refresh_tree()
            self.date_entry.delete(0, tk.END)
            self.generate_text()
            self.current_date_str = date_str
            # Remove or comment out the message box line below
            # messagebox.showinfo("Date Added", f"Date '{date_str}' added and selected.")

    def on_remove_date(self):
        if not self.current_date_str:
            messagebox.showerror("Selection Error", "Please select a date to remove.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the date '{self.current_date_str}'?")
        if confirm:
            success = self.controller.remove_date(self.current_date_str)
            if success:
                self.refresh_tree()
                self.current_date_str = None
                self.generate_text()

    def on_add_group(self):
        group_name = self.group_name_entry.get().strip()
        if not group_name or not self.current_date_str:
            messagebox.showerror("Input Error", "Group name and date selection are required.")
            return
        success = self.controller.add_group(self.current_date_str, group_name)
        if success:
            self.refresh_tree()
            self.group_name_entry.delete(0, tk.END)
            self.generate_text()
            # Optionally set current_group_name
            self.current_group_name = group_name

    def on_remove_group(self):
        if not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Selection Error", "Please select a group to remove.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the group '{self.current_group_name}'?")
        if confirm:
            success = self.controller.remove_group(self.current_date_str, self.current_group_name)
            if success:
                self.refresh_tree()
                self.current_group_name = None
                self.generate_text()

    def on_add_meeting(self):
        meeting_name = self.meeting_name_entry.get().strip()
        location = self.meeting_location_entry.get().strip()
        if not meeting_name or not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Input Error", "Meeting name, group, and date selection are required.")
            return
        success = self.controller.add_meeting(
            self.current_date_str,
            self.current_group_name,
            meeting_name,
            location
        )
        if success:
            self.refresh_tree()
            self.meeting_name_entry.delete(0, tk.END)
            self.meeting_location_entry.delete(0, tk.END)
            self.generate_text()

    def on_remove_meeting(self):
        if not self.current_meeting_name or not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Selection Error", "Please select a meeting to remove.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the meeting '{self.current_meeting_name}'?")
        if confirm:
            success = self.controller.remove_meeting(self.current_date_str, self.current_group_name, self.current_meeting_name)
            if success:
                self.refresh_tree()
                self.current_meeting_name = None
                self.generate_text()

    def on_add_event(self):
        event_name = self.event_name_entry.get().strip()

        # Construct Start Time
        start_hour = self.start_hour_var.get()
        start_minute = self.start_minute_var.get()
        start_am_pm = self.start_am_pm_var.get()
        if not start_hour or not start_minute or not start_am_pm:
            messagebox.showerror("Input Error", "Please select a valid start time.")
            return
        start_time = f"{start_hour}:{start_minute} {start_am_pm}"

        # Construct End Time
        end_hour = self.end_hour_var.get()
        end_minute = self.end_minute_var.get()
        end_am_pm = self.end_am_pm_var.get()
        if end_hour and end_minute and end_am_pm:
            end_time = f"{end_hour}:{end_minute} {end_am_pm}"
        else:
            end_time = ''

        # Validate inputs
        if not event_name or not self.current_meeting_name or not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Input Error", "Event name, meeting, group, and date selection are required.")
            return

        # Prepare event data
        event_data = {
            'event_name': event_name,
            'start_time': start_time,
            'end_time': end_time
        }

        # Add event via controller
        success = self.controller.add_event(
            self.current_date_str,
            self.current_group_name,
            self.current_meeting_name,
            event_data
        )

        if success:
            self.refresh_tree()
            self.clear_event_entries()
            self.generate_text()

    def on_remove_event(self):
        if not self.current_event_name or not self.current_meeting_name or not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Selection Error", "Please select an event to remove.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the event '{self.current_event_name}'?")
        if confirm:
            success = self.controller.remove_event(
                self.current_date_str,
                self.current_group_name,
                self.current_meeting_name,
                self.current_event_name
            )
            if success:
                self.refresh_tree()
                self.current_event_name = None
                self.generate_text()

    def refresh_tree(self):
        # Save the current selection path
        selected_item = self.tree.focus()
        selection_path = self.get_item_path(selected_item)

        # Save the expanded state of all items
        expanded_items = self.get_expanded_items()

        # Clear the tree
        self.tree.delete(*self.tree.get_children())

        # Rebuild the tree
        for date in self.controller.get_all_dates():
            date_id = self.tree.insert('', 'end', text=date.date_str, tags=('date',))
            for group in date.get_all_groups():
                group_id = self.tree.insert(date_id, 'end', text=group.name, tags=('group',))
                for meeting in group.get_all_meetings():
                    meeting_id = self.tree.insert(group_id, 'end', text=meeting.name, tags=('meeting',))
                    for event in meeting.get_all_events():
                        event_details = f"{event.start_time} - {event.end_time}"
                        self.tree.insert(
                            meeting_id,
                            'end',
                            text=event.name,
                            values=(event_details,),
                            tags=('event',)
                        )

        # Restore the expanded state
        if expanded_items:
            self.restore_expanded_items(expanded_items)

        # Restore the previous selection
        if selection_path:
            self.select_item_by_path(selection_path)

    def get_expanded_items(self):
        """Returns a set of item paths that are expanded."""
        expanded = set()

        def _recursively_check_items(item, path):
            if self.tree.item(item, 'open'):
                item_text = self.tree.item(item, 'text')
                new_path = path + (item_text,)
                expanded.add(new_path)
                for child in self.tree.get_children(item):
                    _recursively_check_items(child, new_path)

        for item in self.tree.get_children():
            _recursively_check_items(item, ())

        return expanded

    def restore_expanded_items(self, expanded_items):
        """Expands items whose path is in the expanded_items set."""
        def _recursively_expand_items(item, path):
            item_text = self.tree.item(item, 'text')
            new_path = path + (item_text,)
            if new_path in expanded_items:
                self.tree.item(item, open=True)
                for child in self.tree.get_children(item):
                    _recursively_expand_items(child, new_path)

        for item in self.tree.get_children():
            _recursively_expand_items(item, ())

    def get_item_path(self, item):
        """Returns the path (tuple of texts) from the root to the specified item."""
        path = []
        while item:
            text = self.tree.item(item, 'text')
            path.insert(0, text)
            item = self.tree.parent(item)
        return tuple(path)

    def select_item_by_path(self, path):
        """Selects the item in the tree that matches the given path."""
        parent = ''
        item_id = ''
        for node_text in path:
            found = False
            for child_id in self.tree.get_children(parent):
                child_text = self.tree.item(child_id, 'text')
                if child_text == node_text:
                    parent = child_id
                    item_id = child_id
                    found = True
                    break
            if not found:
                # Could not find the item; stop attempting to select
                return
        if item_id:
            self.tree.focus(item_id)
            self.tree.selection_set(item_id)
            self.tree.see(item_id)

    def clear_event_entries(self):
        self.event_name_entry.delete(0, tk.END)
        # Reset time variables
        self.start_hour_var.set('01')
        self.start_minute_var.set('00')
        self.start_am_pm_var.set('AM')
        self.end_hour_var.set('01')
        self.end_minute_var.set('00')
        self.end_am_pm_var.set('AM')

    def populate_event_entries(self, event_data):
        self.event_name_entry.delete(0, tk.END)
        self.event_name_entry.insert(0, event_data['event_name'])
        self.event_start_time_entry.delete(0, tk.END)
        self.event_start_time_entry.insert(0, event_data['start_time'])
        self.event_end_time_entry.delete(0, tk.END)
        self.event_end_time_entry.insert(0, event_data['end_time'])

    def generate_text(self):
        formatted_text = self.controller.generate_formatted_text()
        self.preview_view.update_preview(formatted_text)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def on_add_notes(self):
        equipment = self.equipment_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip()

        if not self.current_meeting_name or not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Input Error", "Please select a meeting to add equipment and notes.")
            return

        success = self.controller.add_equipment_notes_to_meeting(
            self.current_date_str,
            self.current_group_name,
            self.current_meeting_name,
            equipment,
            notes
        )
        if success:
            self.clear_equipment_entries()
            self.generate_text()
            # Remove or comment out the message box line below
            # messagebox.showinfo("Success", "Equipment and Notes added to the meeting.")

    def on_remove_notes(self):
        if not self.current_meeting_name or not self.current_group_name or not self.current_date_str:
            messagebox.showerror("Input Error", "Please select a meeting to remove equipment and notes.")
            return

        success = self.controller.remove_equipment_notes_from_meeting(
            self.current_date_str,
            self.current_group_name,
            self.current_meeting_name
        )
        if success:
            self.clear_equipment_entries()
            self.generate_text()
            messagebox.showinfo("Success", "Equipment and Notes removed from the meeting.")

    def clear_equipment_entries(self):
        self.equipment_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)

    def create_tree_view(self, parent):
        self.tree = ttk.Treeview(parent)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
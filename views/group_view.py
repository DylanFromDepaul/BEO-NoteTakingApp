import tkinter as tk
from tkinter import messagebox

class GroupView(tk.Frame):
    """
    Manages group-related UI components.
    """

    def __init__(self, master=None, event_view=None):
        super().__init__(master)
        self.event_view = event_view  # Reference to the EventView
        self.selected_group_name = None
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize callbacks
        self.on_add_group_callback = None
        self.on_remove_group_callback = None
        self.on_group_select_callback = None

        self.create_widgets()

    def create_widgets(self):
        # Group Entry
        tk.Label(self, text="Group Name:").pack()
        self.group_entry = tk.Entry(self)
        self.group_entry.pack()

        # Add Group Button
        self.add_group_button = tk.Button(self, text="Add Group", command=self.on_add_group)
        self.add_group_button.pack()

        # Remove Group Button
        self.remove_group_button = tk.Button(self, text="Remove Group", command=self.on_remove_group)
        self.remove_group_button.pack()

        # Group List
        tk.Label(self, text="Groups:").pack()
        self.group_listbox = tk.Listbox(self)
        self.group_listbox.pack(fill=tk.BOTH, expand=True)
        self.group_listbox.bind('<<ListboxSelect>>', self.on_group_select)

    def bind_add_group(self, callback):
        """
        Binds the add group action to the controller's callback.
        """
        self.on_add_group_callback = callback

    def bind_remove_group(self, callback):
        """
        Binds the remove group action to the controller's callback.
        """
        self.on_remove_group_callback = callback

    def on_add_group(self):
        """
        Triggered when the user clicks the 'Add Group' button.
        """
        group_name = self.group_entry.get()
        if group_name and self.on_add_group_callback:
            self.on_add_group_callback(group_name)
            self.group_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter a group name.")

    def on_remove_group(self):
        """
        Triggered when the user clicks the 'Remove Group' button.
        """
        selected_indices = self.group_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            group_name = self.group_listbox.get(index)
            if self.on_remove_group_callback:
                self.on_remove_group_callback(group_name)
        else:
            messagebox.showerror("Selection Error", "Please select a group to remove.")

    def update_group_list(self, groups):
        """
        Updates the group list displayed in the listbox.
        """
        self.group_listbox.delete(0, tk.END)
        for group in groups:
            self.group_listbox.insert(tk.END, group.name)

        # Reselect the previously selected group if it still exists
        if self.selected_group_name in [group.name for group in groups]:
            index = [group.name for group in groups].index(self.selected_group_name)
            self.group_listbox.select_set(index)
        else:
            self.selected_group_name = None

    def on_group_select(self, event):
        """
        Triggered when the user selects a group from the listbox.
        """
        selected_indices = self.group_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            group_name = self.group_listbox.get(index)
            self.selected_group_name = group_name
            if self.on_group_select_callback:
                self.on_group_select_callback(group_name)
            if self.event_view:
                self.event_view.set_selected_group(group_name)
        else:
            self.selected_group_name = None
            if self.event_view:
                self.event_view.set_selected_group(None)

    def bind_group_select(self, callback):
        """
        Binds the group selection action to the controller's callback.
        """
        self.on_group_select_callback = callback

    def get_selected_group(self):
        return self.selected_group_name

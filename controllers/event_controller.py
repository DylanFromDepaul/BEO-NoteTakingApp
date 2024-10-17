import tkinter as tk
from models.event import Event

class EventController:
    """
    Handles event-related operations.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Bind view events to controller methods
        self.view.bind_add_event(self.add_event)

    def add_event(self, group_name, event_details):
        group = self.model.get_group_by_name(group_name)
        if group:
            event = Event(
                name=event_details['event_name'],
                start_time=event_details['start_time'],
                end_time=event_details.get('end_time'),
                location=event_details.get('location'),
                equipment=event_details.get('equipment'),
                notes=event_details.get('notes'),
            )
            group.add_event(event)
            self.view.update_event_list(group.get_event_list())
        else:
            tk.messagebox.showerror("Group Error", f"Group '{group_name}' not found.")

    def update_event(self, event_data):
        group_name = self.view.group_view.get_selected_group()
        if group_name:
            event = self.model.get_event_by_name(group_name, event_data['event_name'])
            if event:
                event.name = event_data['event_name']
                event.start_time = event_data['start_time']
                event.end_time = event_data.get('end_time')
                event.location = event_data.get('location')
                event.equipment = event_data.get('equipment')
                event.notes = event_data.get('notes')
                self.view.update_event_list(self.model.get_group_by_name(group_name).get_event_list())
            else:
                tk.messagebox.showerror("Event Error", f"Event '{event_data['event_name']}' not found in group '{group_name}'.")

    def remove_event(self, event_name):
        group_name = self.view.group_view.get_selected_group()
        if group_name:
            event = self.model.get_event_by_name(group_name, event_name)
            if event:
                self.model.remove_event(group_name, event_name)
                self.view.update_event_list(self.model.get_group_by_name(group_name).get_event_list())
            else:
                tk.messagebox.showerror("Event Error", f"Event '{event_name}' not found in group '{group_name}'.")

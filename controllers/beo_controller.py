from models.date import Date
from models.group import Group
from models.meeting import Meeting
from models.event import Event

class BEOController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_all_dates(self):
        return self.model.get_all_dates()

    def add_date(self, date_str):
        if not date_str:
            self.view.show_error_message("Date cannot be empty.")
            return False
        if self.model.get_date_by_str(date_str):
            self.view.show_error_message(f"Date '{date_str}' already exists.")
            return False
        self.model.add_date(Date(date_str))
        return True

    def remove_date(self, date_str):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        self.model.remove_date(date)
        return True

    def add_group(self, date_str, group_name):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        if date.get_group_by_name(group_name):
            self.view.show_error_message(f"Group '{group_name}' already exists on date '{date_str}'.")
            return False
        date.add_group(Group(group_name))
        return True

    def remove_group(self, date_str, group_name):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        date.remove_group(group)
        return True

    def add_meeting(self, date_str, group_name, meeting_name, location='', equipment='', notes=''):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        if group.get_meeting_by_name(meeting_name):
            self.view.show_error_message(f"Meeting '{meeting_name}' already exists in group '{group_name}'.")
            return False
        group.add_meeting(Meeting(meeting_name, location, notes, equipment))
        return True

    def remove_meeting(self, date_str, group_name, meeting_name):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        meeting = group.get_meeting_by_name(meeting_name)
        if not meeting:
            self.view.show_error_message(f"Meeting '{meeting_name}' not found in group '{group_name}'.")
            return False
        group.remove_meeting(meeting)
        return True

    def add_event(self, date_str, group_name, meeting_name, event_data):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        meeting = group.get_meeting_by_name(meeting_name)
        if not meeting:
            self.view.show_error_message(f"Meeting '{meeting_name}' not found in group '{group_name}'.")
            return False
        event_name = event_data.get('event_name')
        if meeting.get_event_by_name(event_name):
            self.view.show_error_message(f"Event '{event_name}' already exists in meeting '{meeting_name}'.")
            return False
        event = Event(
            name=event_name,
            start_time=event_data.get('start_time', ''),
            end_time=event_data.get('end_time', '')
        )
        meeting.add_event(event)
        return True

    def remove_event(self, date_str, group_name, meeting_name, event_name):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        meeting = group.get_meeting_by_name(meeting_name)
        if not meeting:
            self.view.show_error_message(f"Meeting '{meeting_name}' not found in group '{group_name}'.")
            return False
        event = meeting.get_event_by_name(event_name)
        if not event:
            self.view.show_error_message(f"Event '{event_name}' not found in meeting '{meeting_name}'.")
            return False
        meeting.remove_event(event)
        return True

    def get_event(self, date_str, group_name, meeting_name, event_name):
        date = self.model.get_date_by_str(date_str)
        if not date:
            return None
        group = date.get_group_by_name(group_name)
        if not group:
            return None
        meeting = group.get_meeting_by_name(meeting_name)
        if not meeting:
            return None
        event = meeting.get_event_by_name(event_name)
        if event:
            return {
                'event_name': event.name,
                'start_time': event.start_time,
                'end_time': event.end_time
            }
        else:
            return None

    def generate_formatted_text(self):
        formatted_text = ""
        for date in self.model.get_all_dates():
            formatted_text += f"{date.date_str}\n\n"

            # Add "Groups In House" section
            formatted_text += "Groups In House:\n"
            for group in date.get_all_groups():
                formatted_text += f"{group.name}\n"
            formatted_text += "\n"

            # Now detail each group, meeting, and events
            for group in date.get_all_groups():
                formatted_text += f"{group.name}\n"
                for meeting in group.get_all_meetings():
                    formatted_text += f"{meeting.name}\n"
                    if meeting.location:
                        formatted_text += f"Location: {meeting.location}\n"

                    # Place event details above equipment and notes
                    for event in meeting.get_all_events():
                        event_details = f"{event.start_time} - {event.end_time}"
                        formatted_text += f"{event.name}: {event_details}\n"

                    if meeting.equipment:
                        formatted_text += f"Equipment: {meeting.equipment}\n"
                    if meeting.notes:
                        formatted_text += f"{meeting.notes}\n"
                    formatted_text += "\n"
                formatted_text += "\n"
            formatted_text += "\n"
        return formatted_text.strip()

    def add_equipment_notes_to_meeting(self, date_str, group_name, meeting_name, equipment, notes):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        meeting = group.get_meeting_by_name(meeting_name)
        if not meeting:
            self.view.show_error_message(f"Meeting '{meeting_name}' not found in group '{group_name}'.")
            return False

        # Update the equipment and notes of the meeting
        meeting.equipment = equipment
        meeting.notes = notes
        return True

    def remove_equipment_notes_from_meeting(self, date_str, group_name, meeting_name):
        date = self.model.get_date_by_str(date_str)
        if not date:
            self.view.show_error_message(f"Date '{date_str}' not found.")
            return False
        group = date.get_group_by_name(group_name)
        if not group:
            self.view.show_error_message(f"Group '{group_name}' not found on date '{date_str}'.")
            return False
        meeting = group.get_meeting_by_name(meeting_name)
        if not meeting:
            self.view.show_error_message(f"Meeting '{meeting_name}' not found in group '{group_name}'.")
            return False

        # Clear the equipment and notes
        meeting.equipment = ''
        meeting.notes = ''
        return True

from models.event import Event

class Meeting:
    """
    Represents a meeting within a group.
    """

    def __init__(self, name, location='', notes='', equipment=''):
        self.name = name
        self.location = location
        self.notes = notes
        self.equipment = equipment  # New attribute
        self.events = []  # List of Event objects

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def get_event_by_name(self, name):
        for event in self.events:
            if event.name == name:
                return event
        return None

    def get_all_events(self):
        return self.events

class Event:
    """
    Represents an event within a meeting.
    """

    def __init__(self, name, start_time='', end_time=''):
        self.name = name  # e.g., "Setup", "Meeting"
        self.start_time = start_time
        self.end_time = end_time

from models.meeting import Meeting

class Group:
    def __init__(self, name):
        self.name = name
        self.meetings = []  # List of Meeting objects

    def add_meeting(self, meeting):
        self.meetings.append(meeting)

    def remove_meeting(self, meeting):
        if meeting in self.meetings:
            self.meetings.remove(meeting)

    def get_meeting_by_name(self, name):
        for meeting in self.meetings:
            if meeting.name == name:
                return meeting
        return None

    def get_all_meetings(self):
        return self.meetings

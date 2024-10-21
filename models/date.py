class Date:
    """
    Represents a specific date in the BEO.
    """

    def __init__(self, date_str):
        self.date_str = date_str  # e.g., "Thursday, October 17, 2024"
        self.groups = []  # List of Group objects

    def add_group(self, group):
        self.groups.append(group)

    def remove_group(self, group):
        if group in self.groups:
            self.groups.remove(group)

    def get_group_by_name(self, name):
        for group in self.groups:
            if group.name == name:
                return group
        return None

    def get_all_groups(self):
        return self.groups
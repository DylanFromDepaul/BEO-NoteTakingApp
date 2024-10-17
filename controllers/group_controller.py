from models.group import Group

class GroupController:
    """
    Handles group-related operations, connecting the GroupView to the BEOManager model.
    It controls the logic for adding/removing groups and updating the view.
    """
    
    def __init__(self, model, view):
        """
        Initializes the GroupController.

        :param model: The BEOManager model that manages groups and events.
        :param view: The GroupView that displays and manages group-related UI.
        """
        self.model = model
        self.view = view

        # Bind view events to controller methods
        self.view.bind_add_group(self.add_group)

    def add_group(self, group_name):
        """
        Adds a new group to the BEOManager.

        :param group_name: The name of the group to add.
        """
        group = Group(group_name)
        self.model.add_group(group)
        self.view.update_group_list(self.model.get_all_groups())
        # Notify the event view of the new group
        self.view.event_view.set_current_group(group_name)

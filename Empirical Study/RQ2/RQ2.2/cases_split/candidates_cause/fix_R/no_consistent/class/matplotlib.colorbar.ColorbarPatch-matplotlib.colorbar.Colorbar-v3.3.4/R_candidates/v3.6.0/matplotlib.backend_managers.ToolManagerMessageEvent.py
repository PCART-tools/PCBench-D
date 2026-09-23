class ToolManagerMessageEvent:
    """
    Event carrying messages from toolmanager.

    Messages usually get displayed to the user by the toolbar.
    """
    def __init__(self, name, sender, message):
        self.name = name
        self.sender = sender
        self.message = message

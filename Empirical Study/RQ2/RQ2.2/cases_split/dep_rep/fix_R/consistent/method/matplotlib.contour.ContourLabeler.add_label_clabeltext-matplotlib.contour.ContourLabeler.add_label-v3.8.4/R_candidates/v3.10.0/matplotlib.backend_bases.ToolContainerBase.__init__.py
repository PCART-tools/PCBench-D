    def __init__(self, toolmanager):
        self.toolmanager = toolmanager
        toolmanager.toolmanager_connect(
            'tool_message_event',
            lambda event: self.set_message(event.message))
        toolmanager.toolmanager_connect(
            'tool_removed_event',
            lambda event: self.remove_toolitem(event.tool.name))

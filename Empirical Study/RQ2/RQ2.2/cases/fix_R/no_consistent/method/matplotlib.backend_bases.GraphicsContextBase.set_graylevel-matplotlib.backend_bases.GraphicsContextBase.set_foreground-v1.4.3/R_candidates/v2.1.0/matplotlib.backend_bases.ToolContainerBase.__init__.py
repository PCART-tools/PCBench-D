    def __init__(self, toolmanager):
        self.toolmanager = toolmanager
        self.toolmanager.toolmanager_connect('tool_removed_event',
                                             self._remove_tool_cbk)

    def __init__(self, toolmanager):
        self.toolmanager = toolmanager
        self.toolmanager.toolmanager_connect('tool_message_event',
                                             self._message_cbk)

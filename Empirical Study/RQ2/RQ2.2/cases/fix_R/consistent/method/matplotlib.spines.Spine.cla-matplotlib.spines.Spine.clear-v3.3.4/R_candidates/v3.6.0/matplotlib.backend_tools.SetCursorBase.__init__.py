    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_drag = None
        self._current_tool = None
        self._default_cursor = cursors.POINTER
        self._last_cursor = self._default_cursor
        self.toolmanager.toolmanager_connect('tool_added_event',
                                             self._add_tool_cbk)
        # process current tools
        for tool in self.toolmanager.tools.values():
            self._add_tool(tool)

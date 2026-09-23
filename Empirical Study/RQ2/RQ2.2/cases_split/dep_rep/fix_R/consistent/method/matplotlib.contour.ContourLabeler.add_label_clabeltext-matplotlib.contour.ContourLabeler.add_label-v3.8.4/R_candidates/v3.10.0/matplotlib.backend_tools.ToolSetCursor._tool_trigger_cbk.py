    def _tool_trigger_cbk(self, event):
        self._current_tool = event.tool if event.tool.toggled else None
        self._set_cursor_cbk(event.canvasevent)

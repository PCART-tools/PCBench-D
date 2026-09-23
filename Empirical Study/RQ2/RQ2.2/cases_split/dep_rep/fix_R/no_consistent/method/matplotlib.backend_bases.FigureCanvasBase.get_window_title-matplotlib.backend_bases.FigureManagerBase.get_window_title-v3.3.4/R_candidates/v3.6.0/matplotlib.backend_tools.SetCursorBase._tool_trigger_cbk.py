    def _tool_trigger_cbk(self, event):
        if event.tool.toggled:
            self._current_tool = event.tool
        else:
            self._current_tool = None
        self._set_cursor_cbk(event.canvasevent)

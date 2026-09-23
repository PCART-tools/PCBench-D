    def _tool_trigger_cbk(self, event):
        if event.tool.toggled:
            self._cursor = event.tool.cursor
        else:
            self._cursor = None

        self._set_cursor_cbk(event.canvasevent)

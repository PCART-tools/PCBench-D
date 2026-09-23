    def _remove_tool_cbk(self, event):
        """Captures the 'tool_removed_event' signal and removes the tool."""
        self.remove_toolitem(event.tool.name)

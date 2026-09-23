    def _add_tool_cbk(self, event):
        """Process every newly added tool."""
        if getattr(event.tool, 'cursor', None) is not None:
            self.toolmanager.toolmanager_connect(
                f'tool_trigger_{event.tool.name}', self._tool_trigger_cbk)

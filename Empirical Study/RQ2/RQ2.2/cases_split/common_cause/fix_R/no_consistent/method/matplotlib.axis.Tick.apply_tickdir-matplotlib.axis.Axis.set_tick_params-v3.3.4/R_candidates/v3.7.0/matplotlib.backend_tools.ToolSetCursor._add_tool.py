    def _add_tool(self, tool):
        """Set the cursor when the tool is triggered."""
        if getattr(tool, 'cursor', None) is not None:
            self.toolmanager.toolmanager_connect('tool_trigger_%s' % tool.name,
                                                 self._tool_trigger_cbk)

    def _add_tool_cbk(self, event):
        """Process every newly added tool"""
        if event.tool is self:
            return

        self._add_tool(event.tool)

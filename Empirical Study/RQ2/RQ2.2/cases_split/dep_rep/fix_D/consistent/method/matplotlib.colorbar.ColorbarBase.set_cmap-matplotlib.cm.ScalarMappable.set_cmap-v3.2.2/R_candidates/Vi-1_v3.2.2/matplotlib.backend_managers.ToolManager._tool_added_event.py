    def _tool_added_event(self, tool):
        s = 'tool_added_event'
        event = ToolEvent(s, self, tool)
        self._callbacks.process(s, event)

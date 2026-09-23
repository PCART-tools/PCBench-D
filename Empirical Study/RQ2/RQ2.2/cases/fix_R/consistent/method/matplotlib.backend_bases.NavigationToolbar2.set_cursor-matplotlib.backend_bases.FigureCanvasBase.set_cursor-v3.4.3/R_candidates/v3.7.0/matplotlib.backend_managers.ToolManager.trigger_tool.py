    def trigger_tool(self, name, sender=None, canvasevent=None, data=None):
        """
        Trigger a tool and emit the ``tool_trigger_{name}`` event.

        Parameters
        ----------
        name : str
            Name of the tool.
        sender : object
            Object that wishes to trigger the tool.
        canvasevent : Event
            Original Canvas event or None.
        data : object
            Extra data to pass to the tool when triggering.
        """
        tool = self.get_tool(name)
        if tool is None:
            return

        if sender is None:
            sender = self

        if isinstance(tool, backend_tools.ToolToggleBase):
            self._handle_toggle(tool, canvasevent, data)

        tool.trigger(sender, canvasevent, data)  # Actually trigger Tool.

        s = 'tool_trigger_%s' % name
        event = ToolTriggerEvent(s, sender, tool, canvasevent, data)
        self._callbacks.process(s, event)

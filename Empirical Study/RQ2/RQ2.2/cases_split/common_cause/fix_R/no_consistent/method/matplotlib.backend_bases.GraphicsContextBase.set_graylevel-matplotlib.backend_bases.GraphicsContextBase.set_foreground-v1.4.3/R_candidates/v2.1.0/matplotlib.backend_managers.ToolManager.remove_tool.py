    def remove_tool(self, name):
        """
        Remove tool from `ToolManager`

        Parameters
        ----------
        name : string
            Name of the Tool
        """

        tool = self.get_tool(name)
        tool.destroy()

        # If is a toggle tool and toggled, untoggle
        if getattr(tool, 'toggled', False):
            self.trigger_tool(tool, 'toolmanager')

        self._remove_keys(name)

        s = 'tool_removed_event'
        event = ToolEvent(s, self, tool)
        self._callbacks.process(s, event)

        del self._tools[name]

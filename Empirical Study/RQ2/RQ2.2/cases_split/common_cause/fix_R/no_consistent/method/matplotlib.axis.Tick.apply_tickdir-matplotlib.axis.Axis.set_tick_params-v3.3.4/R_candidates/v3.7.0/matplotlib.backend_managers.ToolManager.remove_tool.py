    def remove_tool(self, name):
        """
        Remove tool named *name*.

        Parameters
        ----------
        name : str
            Name of the tool.
        """

        tool = self.get_tool(name)
        destroy = _api.deprecate_method_override(
            backend_tools.ToolBase.destroy, tool, since="3.6",
            alternative="tool_removed_event")
        if destroy is not None:
            destroy()

        # If it's a toggle tool and toggled, untoggle
        if getattr(tool, 'toggled', False):
            self.trigger_tool(tool, 'toolmanager')

        self._remove_keys(name)

        event = ToolEvent('tool_removed_event', self, tool)
        self._callbacks.process(event.name, event)

        del self._tools[name]

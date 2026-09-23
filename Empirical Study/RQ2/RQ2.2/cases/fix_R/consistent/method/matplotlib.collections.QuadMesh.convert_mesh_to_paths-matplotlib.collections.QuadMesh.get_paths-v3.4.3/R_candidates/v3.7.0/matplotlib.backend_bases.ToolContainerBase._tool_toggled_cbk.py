    def _tool_toggled_cbk(self, event):
        """
        Capture the 'tool_trigger_[name]'

        This only gets used for toggled tools.
        """
        self.toggle_toolitem(event.tool.name, event.tool.toggled)

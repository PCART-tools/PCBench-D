    def _trigger_tool(self, name, sender=None, canvasevent=None, data=None):
        """
        Trigger on a tool

        Method to actually trigger the tool
        """
        tool = self.get_tool(name)

        if isinstance(tool, tools.ToolToggleBase):
            self._handle_toggle(tool, sender, canvasevent, data)

        # Important!!!
        # This is where the Tool object gets triggered
        tool.trigger(sender, canvasevent, data)

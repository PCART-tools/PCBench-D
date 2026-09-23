    def add_tool(self, tool, group, position=-1):
        """
        Adds a tool to this container

        Parameters
        ----------
        tool : tool_like
            The tool to add, see `ToolManager.get_tool`.
        group : str
            The name of the group to add this tool to.
        position : int (optional)
            The position within the group to place this tool.  Defaults to end.
        """
        tool = self.toolmanager.get_tool(tool)
        image = self._get_image_filename(tool.image)
        toggle = getattr(tool, 'toggled', None) is not None
        self.add_toolitem(tool.name, group, position,
                          image, tool.description, toggle)
        if toggle:
            self.toolmanager.toolmanager_connect('tool_trigger_%s' % tool.name,
                                                 self._tool_toggled_cbk)
            # If initially toggled
            if tool.toggled:
                self.toggle_toolitem(tool.name, True)

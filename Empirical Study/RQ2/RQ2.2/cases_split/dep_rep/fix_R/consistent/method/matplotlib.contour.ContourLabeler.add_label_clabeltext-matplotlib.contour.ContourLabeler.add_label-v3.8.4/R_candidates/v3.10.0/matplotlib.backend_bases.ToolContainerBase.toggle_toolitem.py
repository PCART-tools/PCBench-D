    def toggle_toolitem(self, name, toggled):
        """
        A hook to toggle a toolitem without firing an event.

        This hook must be implemented in each backend and contains the
        backend-specific code to silently toggle a toolbar element.

        .. warning::
            This is part of the backend implementation and should
            not be called by end-users.  They should instead call
            `.ToolManager.trigger_tool` or `.ToolContainerBase.trigger_tool`
            (which are equivalent).

        Parameters
        ----------
        name : str
            Id of the tool to toggle.
        toggled : bool
            Whether to set this tool as toggled or not.
        """
        raise NotImplementedError

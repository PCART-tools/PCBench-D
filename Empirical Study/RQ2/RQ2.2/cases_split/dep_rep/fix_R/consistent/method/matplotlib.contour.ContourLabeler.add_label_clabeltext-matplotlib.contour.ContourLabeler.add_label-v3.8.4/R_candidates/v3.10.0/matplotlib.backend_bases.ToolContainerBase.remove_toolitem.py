    def remove_toolitem(self, name):
        """
        A hook to remove a toolitem from the container.

        This hook must be implemented in each backend and contains the
        backend-specific code to remove an element from the toolbar; it is
        called when `.ToolManager` emits a ``tool_removed_event``.

        Because some tools are present only on the `.ToolManager` but not on
        the `ToolContainer`, this method must be a no-op when called on a tool
        absent from the container.

        .. warning::
            This is part of the backend implementation and should
            not be called by end-users.  They should instead call
            `.ToolManager.remove_tool`.

        Parameters
        ----------
        name : str
            Name of the tool to remove.
        """
        raise NotImplementedError

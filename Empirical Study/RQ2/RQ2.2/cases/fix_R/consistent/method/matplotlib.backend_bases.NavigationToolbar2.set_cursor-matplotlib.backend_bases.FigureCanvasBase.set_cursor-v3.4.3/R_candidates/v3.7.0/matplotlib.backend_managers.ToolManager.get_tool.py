    def get_tool(self, name, warn=True):
        """
        Return the tool object with the given name.

        For convenience, this passes tool objects through.

        Parameters
        ----------
        name : str or `.ToolBase`
            Name of the tool, or the tool itself.
        warn : bool, default: True
            Whether a warning should be emitted it no tool with the given name
            exists.

        Returns
        -------
        `.ToolBase` or None
            The tool or None if no tool with the given name exists.
        """
        if (isinstance(name, backend_tools.ToolBase)
                and name.name in self._tools):
            return name
        if name not in self._tools:
            if warn:
                _api.warn_external(
                    f"ToolManager does not control tool {name!r}")
            return None
        return self._tools[name]

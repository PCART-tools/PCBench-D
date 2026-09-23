    def get_tool(self, name, warn=True):
        """
        Return the tool object, also accepts the actual tool for convenience.

        Parameters
        ----------
        name : str, ToolBase
            Name of the tool, or the tool itself
        warn : bool, optional
            If this method should give warnings.
        """
        if isinstance(name, tools.ToolBase) and name.name in self._tools:
            return name
        if name not in self._tools:
            if warn:
                cbook._warn_external("ToolManager does not control tool "
                                     "%s" % name)
            return None
        return self._tools[name]

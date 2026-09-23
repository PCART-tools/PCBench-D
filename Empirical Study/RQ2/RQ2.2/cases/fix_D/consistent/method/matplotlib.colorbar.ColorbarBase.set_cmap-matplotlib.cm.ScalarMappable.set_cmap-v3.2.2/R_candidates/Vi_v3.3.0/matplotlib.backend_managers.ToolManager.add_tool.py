    def add_tool(self, name, tool, *args, **kwargs):
        """
        Add *tool* to `ToolManager`.

        If successful, adds a new event ``tool_trigger_{name}`` where
        ``{name}`` is the *name* of the tool; the event is fired every time the
        tool is triggered.

        Parameters
        ----------
        name : str
            Name of the tool, treated as the ID, has to be unique.
        tool : class_like, i.e. str or type
            Reference to find the class of the Tool to added.

        Notes
        -----
        args and kwargs get passed directly to the tools constructor.

        See Also
        --------
        matplotlib.backend_tools.ToolBase : The base class for tools.
        """

        tool_cls = self._get_cls_to_instantiate(tool)
        if not tool_cls:
            raise ValueError('Impossible to find class for %s' % str(tool))

        if name in self._tools:
            cbook._warn_external('A "Tool class" with the same name already '
                                 'exists, not added')
            return self._tools[name]

        tool_obj = tool_cls(self, name, *args, **kwargs)
        self._tools[name] = tool_obj

        if tool_cls.default_keymap is not None:
            self.update_keymap(name, tool_cls.default_keymap)

        # For toggle tools init the radio_group in self._toggled
        if isinstance(tool_obj, tools.ToolToggleBase):
            # None group is not mutually exclusive, a set is used to keep track
            # of all toggled tools in this group
            if tool_obj.radio_group is None:
                self._toggled.setdefault(None, set())
            else:
                self._toggled.setdefault(tool_obj.radio_group, None)

            # If initially toggled
            if tool_obj.toggled:
                self._handle_toggle(tool_obj, None, None, None)
        tool_obj.set_figure(self.figure)

        self._tool_added_event(tool_obj)
        return tool_obj

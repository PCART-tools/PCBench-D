class SetCursorBase(ToolBase):
    """
    Change to the current cursor while inaxes.

    This tool, keeps track of all `ToolToggleBase` derived tools, and calls
    `set_cursor` when a tool gets triggered.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id_drag = None
        self._cursor = None
        self._default_cursor = cursors.POINTER
        self._last_cursor = self._default_cursor
        self.toolmanager.toolmanager_connect('tool_added_event',
                                             self._add_tool_cbk)

        # process current tools
        for tool in self.toolmanager.tools.values():
            self._add_tool(tool)

    def set_figure(self, figure):
        if self._id_drag:
            self.canvas.mpl_disconnect(self._id_drag)
        super().set_figure(figure)
        if figure:
            self._id_drag = self.canvas.mpl_connect(
                'motion_notify_event', self._set_cursor_cbk)

    def _tool_trigger_cbk(self, event):
        if event.tool.toggled:
            self._cursor = event.tool.cursor
        else:
            self._cursor = None

        self._set_cursor_cbk(event.canvasevent)

    def _add_tool(self, tool):
        """Set the cursor when the tool is triggered."""
        if getattr(tool, 'cursor', None) is not None:
            self.toolmanager.toolmanager_connect('tool_trigger_%s' % tool.name,
                                                 self._tool_trigger_cbk)

    def _add_tool_cbk(self, event):
        """Process every newly added tool."""
        if event.tool is self:
            return
        self._add_tool(event.tool)

    def _set_cursor_cbk(self, event):
        if not event:
            return

        if not getattr(event, 'inaxes', False) or not self._cursor:
            if self._last_cursor != self._default_cursor:
                self.set_cursor(self._default_cursor)
                self._last_cursor = self._default_cursor
        elif self._cursor:
            cursor = self._cursor
            if cursor and self._last_cursor != cursor:
                self.set_cursor(cursor)
                self._last_cursor = cursor

    def set_cursor(self, cursor):
        """
        Set the cursor.

        This method has to be implemented per backend.
        """
        raise NotImplementedError

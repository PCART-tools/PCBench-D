@_api.deprecated("3.5", alternative="ToolSetCursor")
class SetCursorGTK3(backend_tools.SetCursorBase):
    def set_cursor(self, cursor):
        NavigationToolbar2GTK3.set_cursor(
            self._make_classic_style_pseudo_toolbar(), cursor)

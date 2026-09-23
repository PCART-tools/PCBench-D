class SetCursorQt(backend_tools.SetCursorBase):
    def set_cursor(self, cursor):
        NavigationToolbar2QT.set_cursor(
            self._make_classic_style_pseudo_toolbar(), cursor)

class SetCursorWx(backend_tools.SetCursorBase):
    def set_cursor(self, cursor):
        NavigationToolbar2Wx.set_cursor(
            self._make_classic_style_pseudo_toolbar(), cursor)

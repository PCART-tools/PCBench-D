class SetCursorWx(backend_tools.SetCursorBase):
    def set_cursor(self, cursor):
        cursor = wx.Cursor(cursord[cursor])
        self.canvas.SetCursor(cursor)
        self.canvas.Update()

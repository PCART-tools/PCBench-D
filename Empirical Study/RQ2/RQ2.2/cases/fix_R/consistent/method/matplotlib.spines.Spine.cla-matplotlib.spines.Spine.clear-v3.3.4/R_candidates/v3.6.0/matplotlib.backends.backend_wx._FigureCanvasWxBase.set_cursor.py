    def set_cursor(self, cursor):
        # docstring inherited
        cursor = wx.Cursor(_api.check_getitem({
            cursors.MOVE: wx.CURSOR_HAND,
            cursors.HAND: wx.CURSOR_HAND,
            cursors.POINTER: wx.CURSOR_ARROW,
            cursors.SELECT_REGION: wx.CURSOR_CROSS,
            cursors.WAIT: wx.CURSOR_WAIT,
            cursors.RESIZE_HORIZONTAL: wx.CURSOR_SIZEWE,
            cursors.RESIZE_VERTICAL: wx.CURSOR_SIZENS,
        }, cursor=cursor))
        self.SetCursor(cursor)
        self.Refresh()

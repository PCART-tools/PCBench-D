    def set_cursor(self, cursor):
        cursor = wxc.Cursor(cursord[cursor])
        self.canvas.SetCursor(cursor)
        self.canvas.Update()

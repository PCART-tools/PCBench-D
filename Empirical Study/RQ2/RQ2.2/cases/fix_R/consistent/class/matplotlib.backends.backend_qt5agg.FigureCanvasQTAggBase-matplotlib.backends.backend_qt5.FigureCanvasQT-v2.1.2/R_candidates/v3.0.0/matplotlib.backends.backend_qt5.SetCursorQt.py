class SetCursorQt(backend_tools.SetCursorBase):
    def set_cursor(self, cursor):
        self.canvas.setCursor(cursord[cursor])

class SetCursorTk(backend_tools.SetCursorBase):
    def set_cursor(self, cursor):
        self.figure.canvas.manager.window.configure(cursor=cursord[cursor])

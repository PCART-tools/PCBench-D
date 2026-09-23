    def set_cursor(self, cursor):
        try:
            self._tkcanvas.configure(cursor=cursord[cursor])
        except tkinter.TclError:
            pass

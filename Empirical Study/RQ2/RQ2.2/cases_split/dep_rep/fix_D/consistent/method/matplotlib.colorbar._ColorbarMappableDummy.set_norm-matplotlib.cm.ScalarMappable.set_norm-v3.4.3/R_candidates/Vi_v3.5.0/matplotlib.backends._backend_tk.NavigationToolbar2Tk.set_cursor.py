    def set_cursor(self, cursor):
        window = self.canvas.get_tk_widget().master
        try:
            window.configure(cursor=cursord[cursor])
        except tkinter.TclError:
            pass

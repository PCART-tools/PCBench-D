    def set_cursor(self, cursor):
        window = self.canvas.get_tk_widget().master
        window.configure(cursor=cursord[cursor])
        window.update_idletasks()

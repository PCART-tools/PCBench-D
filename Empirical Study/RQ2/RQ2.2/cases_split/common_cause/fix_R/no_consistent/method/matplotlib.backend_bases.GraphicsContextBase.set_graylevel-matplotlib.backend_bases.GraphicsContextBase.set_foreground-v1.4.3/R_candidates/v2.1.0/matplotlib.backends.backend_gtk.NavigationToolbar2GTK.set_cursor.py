    def set_cursor(self, cursor):
        self.canvas.window.set_cursor(cursord[cursor])
        gtk.main_iteration()

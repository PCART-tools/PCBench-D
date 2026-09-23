    def set_cursor(self, cursor):
        window = self.canvas.get_property("window")
        if window is not None:
            window.set_cursor(cursord[cursor])
            Gtk.main_iteration()

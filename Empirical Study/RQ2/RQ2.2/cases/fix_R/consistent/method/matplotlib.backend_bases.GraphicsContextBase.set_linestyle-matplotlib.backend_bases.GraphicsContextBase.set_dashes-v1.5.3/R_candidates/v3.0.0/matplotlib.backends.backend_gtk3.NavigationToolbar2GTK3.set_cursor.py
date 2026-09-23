    def set_cursor(self, cursor):
        self.canvas.get_property("window").set_cursor(cursord[cursor])
        Gtk.main_iteration()

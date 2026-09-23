    def set_cursor(self, cursor):
        # docstring inherited
        self.set_cursor_from_name(_backend_gtk.mpl_to_gtk_cursor_name(cursor))

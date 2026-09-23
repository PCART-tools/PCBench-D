    def set_cursor(self, cursor):
        # docstring inherited
        self.set_cursor_from_name(_mpl_to_gtk_cursor(cursor))

    def set_cursor(self, cursor):
        """Set the current cursor to one of the :class:`Cursors` enums values.

        If required by the backend, this method should trigger an update in
        the backend event loop after the cursor is set, as this method may be
        called e.g. before a long-running task during which the GUI is not
        updated.
        """

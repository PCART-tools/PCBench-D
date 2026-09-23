    @_api.deprecated("3.5", alternative="figure.canvas.set_cursor")
    def set_cursor(self, cursor):
        """
        Set the cursor.
        """
        self.canvas.set_cursor(cursor)

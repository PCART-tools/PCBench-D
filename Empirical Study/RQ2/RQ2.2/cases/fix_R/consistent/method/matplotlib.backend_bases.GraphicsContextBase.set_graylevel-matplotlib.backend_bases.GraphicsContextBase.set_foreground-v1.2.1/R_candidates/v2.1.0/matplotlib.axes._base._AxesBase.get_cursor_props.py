    @cbook.deprecated("2.1")
    def get_cursor_props(self):
        """
        Return the cursor propertiess as a (*linewidth*, *color*)
        tuple, where *linewidth* is a float and *color* is an RGBA
        tuple
        """
        return self._cursorProps

    @cbook.deprecated("3.3", alternative="get_picker")
    def get_contains(self):
        """
        Return the custom contains function of the artist if set, or *None*.

        See Also
        --------
        set_contains
        """
        return self._contains

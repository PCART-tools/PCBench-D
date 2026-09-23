    def pickable(self):
        """
        Return whether the artist is pickable.

        See Also
        --------
        set_picker, get_picker, pick
        """
        return self.figure is not None and self._picker is not None

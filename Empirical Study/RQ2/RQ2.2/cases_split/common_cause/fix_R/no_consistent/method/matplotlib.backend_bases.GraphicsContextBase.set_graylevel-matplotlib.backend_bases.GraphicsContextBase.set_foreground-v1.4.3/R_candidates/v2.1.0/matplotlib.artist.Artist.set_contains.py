    def set_contains(self, picker):
        """
        Replace the contains test used by this artist. The new picker
        should be a callable function which determines whether the
        artist is hit by the mouse event::

            hit, props = picker(artist, mouseevent)

        If the mouse event is over the artist, return *hit* = *True*
        and *props* is a dictionary of properties you want returned
        with the contains test.

        ACCEPTS: a callable function
        """
        self._contains = picker

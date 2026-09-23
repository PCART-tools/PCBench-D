    def set_contains(self, picker):
        """
        Define a custom contains test for the artist.

        The provided callable replaces the default `.contains` method
        of the artist.

        Parameters
        ----------
        picker : callable
            A custom picker function to evaluate if an event is within the
            artist. The function must have the signature::

                def contains(artist: Artist, event: MouseEvent) -> bool, dict

            that returns:

            - a bool indicating if the event is within the artist
            - a dict of additional information. The dict should at least
              return the same information as the default ``contains()``
              implementation of the respective artist, but may provide
              additional information.
        """
        if not callable(picker):
            raise TypeError("picker is not a callable")
        self._contains = picker

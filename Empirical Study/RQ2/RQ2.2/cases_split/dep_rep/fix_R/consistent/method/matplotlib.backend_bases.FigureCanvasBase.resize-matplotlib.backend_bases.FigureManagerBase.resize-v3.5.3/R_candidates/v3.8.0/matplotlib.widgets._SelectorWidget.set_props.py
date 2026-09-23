    def set_props(self, **props):
        """
        Set the properties of the selector artist.

        See the *props* argument in the selector docstring to know which properties are
        supported.
        """
        artist = self._selection_artist
        props = cbook.normalize_kwargs(props, artist)
        artist.set(**props)
        if self.useblit:
            self.update()

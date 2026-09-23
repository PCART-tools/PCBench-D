    @property
    def artists(self):
        """Tuple of the artists of the selector."""
        handles_artists = getattr(self, '_handles_artists', ())
        return (self._selection_artist,) + handles_artists

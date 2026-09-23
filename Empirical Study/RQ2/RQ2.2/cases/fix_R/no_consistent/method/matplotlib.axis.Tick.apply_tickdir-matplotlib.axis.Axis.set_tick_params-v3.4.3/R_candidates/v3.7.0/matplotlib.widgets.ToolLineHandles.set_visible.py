    def set_visible(self, value):
        """Set the visibility state of the handles artist."""
        for artist in self.artists:
            artist.set_visible(value)

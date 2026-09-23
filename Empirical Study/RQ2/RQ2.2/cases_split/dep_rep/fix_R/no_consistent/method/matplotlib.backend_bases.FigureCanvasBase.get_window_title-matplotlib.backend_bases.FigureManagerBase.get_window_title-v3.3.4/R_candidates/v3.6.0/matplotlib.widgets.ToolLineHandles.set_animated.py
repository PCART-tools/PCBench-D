    def set_animated(self, value):
        """Set the animated state of the handles artist."""
        for artist in self.artists:
            artist.set_animated(value)

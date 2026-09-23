    def set_visible(self, visible):
        """Set the visibility of the selector artists."""
        self._visible = visible
        for artist in self.artists:
            artist.set_visible(visible)

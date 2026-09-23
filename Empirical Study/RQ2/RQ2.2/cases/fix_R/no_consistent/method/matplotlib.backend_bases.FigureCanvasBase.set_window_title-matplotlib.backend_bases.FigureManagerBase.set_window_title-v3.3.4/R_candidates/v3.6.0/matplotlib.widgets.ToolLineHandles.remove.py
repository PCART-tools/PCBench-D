    def remove(self):
        """Remove the handles artist from the figure."""
        for artist in self._artists:
            artist.remove()

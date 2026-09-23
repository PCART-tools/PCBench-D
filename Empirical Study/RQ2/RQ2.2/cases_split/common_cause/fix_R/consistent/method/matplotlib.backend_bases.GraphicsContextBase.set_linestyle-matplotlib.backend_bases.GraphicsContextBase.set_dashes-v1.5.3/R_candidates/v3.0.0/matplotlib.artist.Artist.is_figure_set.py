    @cbook.deprecated("2.2", "artist.figure is not None")
    def is_figure_set(self):
        """Returns whether the artist is assigned to a `.Figure`."""
        return self.figure is not None

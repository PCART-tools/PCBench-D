    def _get_position_xy(self, renderer):
        """Return the pixel position of the annotated point."""
        x, y = self.xy
        return self._get_xy(renderer, x, y, self.xycoords)

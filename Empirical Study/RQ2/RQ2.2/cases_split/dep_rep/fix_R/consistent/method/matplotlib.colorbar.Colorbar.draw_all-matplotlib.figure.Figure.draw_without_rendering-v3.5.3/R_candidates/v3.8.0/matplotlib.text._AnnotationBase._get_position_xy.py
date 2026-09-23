    def _get_position_xy(self, renderer):
        """Return the pixel position of the annotated point."""
        return self._get_xy(renderer, self.xy, self.xycoords)

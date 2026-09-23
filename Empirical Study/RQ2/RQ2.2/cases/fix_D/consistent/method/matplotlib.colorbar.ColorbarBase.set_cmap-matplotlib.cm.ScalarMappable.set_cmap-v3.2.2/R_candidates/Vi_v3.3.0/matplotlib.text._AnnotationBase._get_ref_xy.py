    def _get_ref_xy(self, renderer):
        """
        Return x, y (in display coordinates) that is to be used for a reference
        of any offset coordinate.
        """
        return self._get_xy(renderer, *self.xy, self.xycoords)

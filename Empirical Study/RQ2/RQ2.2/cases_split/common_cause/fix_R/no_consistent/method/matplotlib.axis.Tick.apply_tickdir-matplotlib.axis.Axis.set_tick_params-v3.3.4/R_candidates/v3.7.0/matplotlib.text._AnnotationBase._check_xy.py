    def _check_xy(self, renderer=None):
        """Check whether the annotation at *xy_pixel* should be drawn."""
        if renderer is None:
            renderer = self.figure._get_renderer()
        b = self.get_annotation_clip()
        if b or (b is None and self.xycoords == "data"):
            # check if self.xy is inside the axes.
            xy_pixel = self._get_position_xy(renderer)
            return self.axes.contains_point(xy_pixel)
        return True

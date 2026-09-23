    def _check_xy(self, renderer, xy_pixel):
        """
        given the xy pixel coordinate, check if the annotation need to
        be drawn.
        """

        b = self.get_annotation_clip()

        if b or (b is None and self.xycoords == "data"):
            # check if self.xy is inside the axes.
            if not self.axes.contains_point(xy_pixel):
                return False

        return True

    def _check_xy(self, renderer):
        """
        check if the annotation need to
        be drawn.
        """

        b = self.get_annotation_clip()

        if b or (b is None and self.coords1 == "data"):
            x, y = self.xy1
            xy_pixel = self._get_xy(x, y, self.coords1, self.axesA)
            if not self.axes.contains_point(xy_pixel):
                return False

        if b or (b is None and self.coords2 == "data"):
            x, y = self.xy2
            xy_pixel = self._get_xy(x, y, self.coords2, self.axesB)
            if self.axesB is None:
                axes = self.axes
            else:
                axes = self.axesB
            if not axes.contains_point(xy_pixel):
                return False

        return True

    @property
    def center(self):
        """Center of rectangle."""
        x0, y0, width, height = self._rect_bbox
        return x0 + width / 2., y0 + height / 2.

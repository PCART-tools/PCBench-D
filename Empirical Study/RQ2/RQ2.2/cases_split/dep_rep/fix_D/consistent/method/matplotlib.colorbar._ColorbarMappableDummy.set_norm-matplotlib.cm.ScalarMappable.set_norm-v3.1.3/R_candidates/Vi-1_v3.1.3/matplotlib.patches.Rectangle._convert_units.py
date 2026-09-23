    def _convert_units(self):
        """
        Convert bounds of the rectangle.
        """
        x0 = self.convert_xunits(self._x0)
        y0 = self.convert_yunits(self._y0)
        x1 = self.convert_xunits(self._x1)
        y1 = self.convert_yunits(self._y1)
        return x0, y0, x1, y1

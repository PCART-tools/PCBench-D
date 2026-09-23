    @locked_y0.setter
    def locked_y0(self, y0):
        self._locked_points.mask[0, 1] = y0 is None
        self._locked_points.data[0, 1] = y0
        self.invalidate()

    @locked_x0.setter
    def locked_x0(self, x0):
        self._locked_points.mask[0, 0] = x0 is None
        self._locked_points.data[0, 0] = x0
        self.invalidate()

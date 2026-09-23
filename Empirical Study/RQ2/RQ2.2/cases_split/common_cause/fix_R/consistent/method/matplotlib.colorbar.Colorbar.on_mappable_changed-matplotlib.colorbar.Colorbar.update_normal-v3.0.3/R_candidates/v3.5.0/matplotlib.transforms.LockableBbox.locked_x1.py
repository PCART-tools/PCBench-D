    @locked_x1.setter
    def locked_x1(self, x1):
        self._locked_points.mask[1, 0] = x1 is None
        self._locked_points.data[1, 0] = x1
        self.invalidate()

    @locked_y1.setter
    def locked_y1(self, y1):
        self._locked_points.mask[1, 1] = y1 is None
        self._locked_points.data[1, 1] = y1
        self.invalidate()

    @BboxBase.y1.setter
    def y1(self, val):
        self._points[1, 1] = val
        self.invalidate()

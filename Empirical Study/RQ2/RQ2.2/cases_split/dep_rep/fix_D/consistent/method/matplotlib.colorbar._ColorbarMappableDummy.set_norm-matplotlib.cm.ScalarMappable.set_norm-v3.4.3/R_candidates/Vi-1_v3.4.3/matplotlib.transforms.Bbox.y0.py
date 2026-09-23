    @BboxBase.y0.setter
    def y0(self, val):
        self._points[0, 1] = val
        self.invalidate()

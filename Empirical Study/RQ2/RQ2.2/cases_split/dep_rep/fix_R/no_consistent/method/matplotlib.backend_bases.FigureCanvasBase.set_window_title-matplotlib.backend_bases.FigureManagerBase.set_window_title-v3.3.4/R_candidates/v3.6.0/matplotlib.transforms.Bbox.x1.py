    @BboxBase.x1.setter
    def x1(self, val):
        self._points[1, 0] = val
        self.invalidate()

    @BboxBase.x0.setter
    def x0(self, val):
        self._points[0, 0] = val
        self.invalidate()

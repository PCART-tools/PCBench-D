    @BboxBase.p0.setter
    def p0(self, val):
        self._points[0] = val
        self.invalidate()

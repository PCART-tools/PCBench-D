    @BboxBase.p1.setter
    def p1(self, val):
        self._points[1] = val
        self.invalidate()

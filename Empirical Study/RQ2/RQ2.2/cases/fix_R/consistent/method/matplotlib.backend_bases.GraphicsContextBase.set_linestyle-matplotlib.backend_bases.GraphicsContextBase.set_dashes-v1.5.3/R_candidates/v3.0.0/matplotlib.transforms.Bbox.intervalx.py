    @BboxBase.intervalx.setter
    def intervalx(self, interval):
        self._points[:, 0] = interval
        self.invalidate()

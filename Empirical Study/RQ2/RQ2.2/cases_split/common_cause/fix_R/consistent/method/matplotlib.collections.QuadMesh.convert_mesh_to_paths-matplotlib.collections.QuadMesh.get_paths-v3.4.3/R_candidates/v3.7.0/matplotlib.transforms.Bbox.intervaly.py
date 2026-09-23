    @BboxBase.intervaly.setter
    def intervaly(self, interval):
        self._points[:, 1] = interval
        self.invalidate()

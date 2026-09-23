    def set_center(self, center):
        self._path = None
        self.center = center
        self.stale = True

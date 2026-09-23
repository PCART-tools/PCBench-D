    def set_radius(self, radius):
        self._path = None
        self.r = radius
        self.stale = True

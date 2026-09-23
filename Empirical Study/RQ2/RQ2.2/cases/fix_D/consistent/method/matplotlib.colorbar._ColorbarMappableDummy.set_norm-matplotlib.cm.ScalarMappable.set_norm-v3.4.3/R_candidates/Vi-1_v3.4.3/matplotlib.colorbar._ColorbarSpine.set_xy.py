    def set_xy(self, xy):
        self._path = mpath.Path(xy, closed=True)
        self.stale = True

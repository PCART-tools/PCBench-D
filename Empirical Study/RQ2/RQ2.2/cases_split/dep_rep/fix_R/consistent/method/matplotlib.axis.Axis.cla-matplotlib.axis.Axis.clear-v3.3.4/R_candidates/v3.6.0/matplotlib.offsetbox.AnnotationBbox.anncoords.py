    @anncoords.setter
    def anncoords(self, coords):
        self.boxcoords = coords
        self.stale = True

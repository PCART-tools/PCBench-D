    def _init(self):
        self._lut = np.ones((self.N + 3, 4), float)
        self._lut[:-3, 0] = makeMappingArray(
            self.N, self._segmentdata['red'], self._gamma)
        self._lut[:-3, 1] = makeMappingArray(
            self.N, self._segmentdata['green'], self._gamma)
        self._lut[:-3, 2] = makeMappingArray(
            self.N, self._segmentdata['blue'], self._gamma)
        if 'alpha' in self._segmentdata:
            self._lut[:-3, 3] = makeMappingArray(
                self.N, self._segmentdata['alpha'], 1)
        self._isinit = True
        self._set_extremes()

    def _init(self):
        rgba = colorConverter.to_rgba_array(self.colors)
        self._lut = np.zeros((self.N + 3, 4), float)
        self._lut[:-3] = rgba
        self._isinit = True
        self._set_extremes()

    def __eq__(self, other):
        if not isinstance(other, BivarColormap):
            return False
        # To compare lookup tables the Colormaps have to be initialized
        if not self._isinit:
            self._init()
        if not other._isinit:
            other._init()
        if not np.array_equal(self._lut, other._lut):
            return False
        if not np.array_equal(self._rgba_bad, other._rgba_bad):
            return False
        if not np.array_equal(self._rgba_outside, other._rgba_outside):
            return False
        if self.shape != other.shape:
            return False
        return True

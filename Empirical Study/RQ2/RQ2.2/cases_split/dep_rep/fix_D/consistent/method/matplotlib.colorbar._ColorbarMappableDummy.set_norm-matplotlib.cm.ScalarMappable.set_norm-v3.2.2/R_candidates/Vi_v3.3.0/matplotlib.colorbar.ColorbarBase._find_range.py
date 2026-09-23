    def _find_range(self):
        """
        Set :attr:`vmin` and :attr:`vmax` attributes to the first and
        last boundary excluding extended end boundaries.
        """
        b = self._boundaries[self._inside]
        self.vmin = b[0]
        self.vmax = b[-1]

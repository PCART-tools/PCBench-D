    def _inverse_boundaries(self, x):
        b = self._boundaries
        return np.interp(x, np.linspace(0, b[-1], len(b)), b)

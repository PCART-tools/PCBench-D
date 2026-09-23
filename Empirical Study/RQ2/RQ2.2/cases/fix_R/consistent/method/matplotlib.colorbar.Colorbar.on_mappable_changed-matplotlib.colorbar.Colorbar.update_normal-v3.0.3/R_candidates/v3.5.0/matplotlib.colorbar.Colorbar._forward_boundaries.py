    def _forward_boundaries(self, x):
        b = self._boundaries
        y = np.interp(x, b, np.linspace(0, b[-1], len(b)))
        eps = (b[-1] - b[0]) * 1e-6
        y[x < b[0]-eps] = -1
        y[x > b[-1]+eps] = 2
        return y

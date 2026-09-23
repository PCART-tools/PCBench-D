    def gt(self, x):
        'return the smallest multiple of base > x'
        d, m = divmod(x, self._base)
        if closeto(m / self._base, 1):
            #looks like floating point error
            return (d + 2) * self._base
        return (d + 1) * self._base

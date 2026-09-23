    def le(self, x):
        'return the largest multiple of base <= x'
        d, m = _divmod(x, self._base)
        if closeto(m / self._base, 1):  # was closeto(m, self._base)
            #looks like floating point error
            return (d + 1) * self._base
        return d * self._base

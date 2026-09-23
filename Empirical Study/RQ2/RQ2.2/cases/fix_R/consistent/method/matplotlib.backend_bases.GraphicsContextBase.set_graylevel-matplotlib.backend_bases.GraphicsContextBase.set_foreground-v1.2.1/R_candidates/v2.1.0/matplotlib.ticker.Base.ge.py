    def ge(self, x):
        'return the smallest multiple of base >= x'
        d, m = _divmod(x, self._base)
        if closeto(m, 0) and not closeto(m / self._base, 1):
            return d * self._base
        return (d + 1) * self._base

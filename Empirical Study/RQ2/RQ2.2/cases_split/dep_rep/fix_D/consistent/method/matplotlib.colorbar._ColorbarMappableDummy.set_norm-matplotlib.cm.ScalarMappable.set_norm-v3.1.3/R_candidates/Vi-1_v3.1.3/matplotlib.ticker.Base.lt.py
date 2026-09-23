    def lt(self, x):
        'return the largest multiple of base < x'
        d, m = divmod(x, self._base)
        if closeto(m, 0) and not closeto(m / self._base, 1):
            return (d - 1) * self._base
        return d * self._base

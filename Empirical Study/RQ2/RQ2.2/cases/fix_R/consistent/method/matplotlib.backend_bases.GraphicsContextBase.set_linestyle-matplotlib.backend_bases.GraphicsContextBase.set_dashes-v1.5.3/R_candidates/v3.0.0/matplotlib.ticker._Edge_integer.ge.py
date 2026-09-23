    def ge(self, x):
        'Return the smallest n: n*step >= x.'
        d, m = _divmod(x, self.step)
        if self.closeto(m / self.step, 0):
            return d
        return (d + 1)

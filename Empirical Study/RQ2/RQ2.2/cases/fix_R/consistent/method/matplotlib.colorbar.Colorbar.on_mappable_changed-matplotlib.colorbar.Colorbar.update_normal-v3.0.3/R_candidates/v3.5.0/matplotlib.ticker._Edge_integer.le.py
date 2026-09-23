    def le(self, x):
        """Return the largest n: n*step <= x."""
        d, m = divmod(x, self.step)
        if self.closeto(m / self.step, 1):
            return d + 1
        return d

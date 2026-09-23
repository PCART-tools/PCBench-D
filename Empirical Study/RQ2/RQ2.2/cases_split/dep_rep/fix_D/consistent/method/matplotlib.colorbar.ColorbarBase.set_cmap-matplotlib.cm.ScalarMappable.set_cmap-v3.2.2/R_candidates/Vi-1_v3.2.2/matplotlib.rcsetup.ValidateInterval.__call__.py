    def __call__(self, s):
        try:
            s = float(s)
        except ValueError:
            raise RuntimeError('Value must be a float; found "%s"' % s)

        if self.cmin and s < self.vmin:
            raise RuntimeError('Value must be >= %f; found "%f"' %
                               (self.vmin, s))
        elif not self.cmin and s <= self.vmin:
            raise RuntimeError('Value must be > %f; found "%f"' %
                               (self.vmin, s))

        if self.cmax and s > self.vmax:
            raise RuntimeError('Value must be <= %f; found "%f"' %
                               (self.vmax, s))
        elif not self.cmax and s >= self.vmax:
            raise RuntimeError('Value must be < %f; found "%f"' %
                               (self.vmax, s))
        return s

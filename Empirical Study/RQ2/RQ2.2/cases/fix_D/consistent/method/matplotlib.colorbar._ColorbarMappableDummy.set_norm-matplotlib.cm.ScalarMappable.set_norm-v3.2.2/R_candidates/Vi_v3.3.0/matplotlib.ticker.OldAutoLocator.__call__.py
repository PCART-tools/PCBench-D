    def __call__(self):
        # docstring inherited
        vmin, vmax = self.axis.get_view_interval()
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        d = abs(vmax - vmin)
        locator = self.get_locator(d)
        return self.raise_if_exceeds(locator())

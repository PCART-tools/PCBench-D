    def refresh(self):
        # docstring inherited
        vmin, vmax = self.axis.get_view_interval()
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        d = abs(vmax - vmin)
        self._locator = self.get_locator(d)

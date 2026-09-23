    def refresh(self):
        # docstring inherited
        dmin, dmax = self.viewlim_to_dt()
        self._locator = self.get_locator(dmin, dmax)

    def refresh(self):
        'Refresh internal information based on current limits.'
        dmin, dmax = self.viewlim_to_dt()
        self._locator = self.get_locator(dmin, dmax)

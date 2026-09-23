    @cbook.deprecated("3.2")
    def autoscale(self):
        'Try to choose the view limits intelligently.'
        dmin, dmax = self.datalim_to_dt()
        self._locator = self.get_locator(dmin, dmax)
        return self._locator.autoscale()

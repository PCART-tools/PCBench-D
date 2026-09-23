    def set_major_locator(self, locator):
        """
        Set the locator of the major ticker.

        Parameters
        ----------
        locator : `~matplotlib.ticker.Locator`
        """
        _api.check_isinstance(mticker.Locator, locator=locator)
        self.isDefault_majloc = False
        self.major.locator = locator
        if self.major.formatter:
            self.major.formatter._set_locator(locator)
        locator.set_axis(self)
        self.stale = True

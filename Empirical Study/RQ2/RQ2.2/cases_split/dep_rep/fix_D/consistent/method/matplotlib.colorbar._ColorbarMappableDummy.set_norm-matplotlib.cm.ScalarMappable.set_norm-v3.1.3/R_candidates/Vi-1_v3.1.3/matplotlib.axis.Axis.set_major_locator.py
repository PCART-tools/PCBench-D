    def set_major_locator(self, locator):
        """
        Set the locator of the major ticker.

        Parameters
        ----------
        locator : `~matplotlib.ticker.Locator`
        """
        if not isinstance(locator, mticker.Locator):
            raise TypeError("locator argument should be instance of "
                            "matplotlib.ticker.Locator")
        self.isDefault_majloc = False
        self.major.locator = locator
        if self.major.formatter:
            self.major.formatter._set_locator(locator)
        locator.set_axis(self)
        self.stale = True

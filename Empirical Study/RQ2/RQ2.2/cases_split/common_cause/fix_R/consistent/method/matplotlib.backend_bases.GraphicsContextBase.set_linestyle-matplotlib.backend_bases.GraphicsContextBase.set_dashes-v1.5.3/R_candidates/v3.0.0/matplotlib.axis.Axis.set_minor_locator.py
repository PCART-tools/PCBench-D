    def set_minor_locator(self, locator):
        """
        Set the locator of the minor ticker.

        Parameters
        ----------
        locator : ~matplotlib.ticker.Locator
        """
        if not isinstance(locator, mticker.Locator):
            raise TypeError("formatter argument should be instance of "
                    "matplotlib.ticker.Locator")
        self.isDefault_minloc = False
        self.minor.locator = locator
        locator.set_axis(self)
        self.stale = True

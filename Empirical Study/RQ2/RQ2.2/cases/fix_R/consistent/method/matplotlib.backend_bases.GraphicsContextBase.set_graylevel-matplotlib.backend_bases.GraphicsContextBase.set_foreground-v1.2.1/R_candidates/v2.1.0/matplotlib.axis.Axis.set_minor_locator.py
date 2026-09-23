    def set_minor_locator(self, locator):
        """
        Set the locator of the minor ticker

        ACCEPTS: a :class:`~matplotlib.ticker.Locator` instance
        """
        self.isDefault_minloc = False
        self.minor.locator = locator
        locator.set_axis(self)
        self.stale = True

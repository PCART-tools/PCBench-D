    def set_major_locator(self, locator):
        """
        Set the locator of the major ticker

        ACCEPTS: a :class:`~matplotlib.ticker.Locator` instance
        """
        self.isDefault_majloc = False
        self.major.locator = locator
        locator.set_axis(self)
        self.stale = True

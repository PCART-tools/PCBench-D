    def set_ticks(self, ticks, update_ticks=True):
        """
        Set tick locations.

        Parameters
        ----------
        ticks : array-like or `~matplotlib.ticker.Locator` or None
            The tick positions can be hard-coded by an array of values; or
            they can be defined by a `.Locator`. Setting to *None* reverts
            to using a default locator.

        update_ticks : bool, default: True
            If True, tick locations are updated immediately.  If False, the
            user has to call `update_ticks` later to update the ticks.

        """
        if np.iterable(ticks):
            self.locator = ticker.FixedLocator(ticks, nbins=len(ticks))
        else:
            self.locator = ticks

        if update_ticks:
            self.update_ticks()
        self.stale = True

    def set_ticks(self, ticks, update_ticks=True):
        """
        Set tick locations.

        Parameters
        ----------
        ticks : {None, sequence, :class:`~matplotlib.ticker.Locator` instance}
            If None, a default Locator will be used.

        update_ticks : {True, False}, optional
            If True, tick locations are updated immediately.  If False,
            use :meth:`update_ticks` to manually update the ticks.

        """
        if np.iterable(ticks):
            self.locator = ticker.FixedLocator(ticks, nbins=len(ticks))
        else:
            self.locator = ticks

        if update_ticks:
            self.update_ticks()
        self.stale = True

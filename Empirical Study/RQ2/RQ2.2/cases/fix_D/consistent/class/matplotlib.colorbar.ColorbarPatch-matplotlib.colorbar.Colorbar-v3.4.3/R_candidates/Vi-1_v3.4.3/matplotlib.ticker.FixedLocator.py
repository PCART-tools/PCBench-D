class FixedLocator(Locator):
    """
    Tick locations are fixed.  If nbins is not None,
    the array of possible positions will be subsampled to
    keep the number of ticks <= nbins +1.
    The subsampling will be done so as to include the smallest
    absolute value; for example, if zero is included in the
    array of possibilities, then it is guaranteed to be one of
    the chosen ticks.
    """

    def __init__(self, locs, nbins=None):
        self.locs = np.asarray(locs)
        self.nbins = max(nbins, 2) if nbins is not None else None

    def set_params(self, nbins=None):
        """Set parameters within this locator."""
        if nbins is not None:
            self.nbins = nbins

    def __call__(self):
        return self.tick_values(None, None)

    def tick_values(self, vmin, vmax):
        """
        Return the locations of the ticks.

        .. note::

            Because the values are fixed, vmin and vmax are not used in this
            method.

        """
        if self.nbins is None:
            return self.locs
        step = max(int(np.ceil(len(self.locs) / self.nbins)), 1)
        ticks = self.locs[::step]
        for i in range(1, step):
            ticks1 = self.locs[i::step]
            if np.abs(ticks1).min() < np.abs(ticks).min():
                ticks = ticks1
        return self.raise_if_exceeds(ticks)

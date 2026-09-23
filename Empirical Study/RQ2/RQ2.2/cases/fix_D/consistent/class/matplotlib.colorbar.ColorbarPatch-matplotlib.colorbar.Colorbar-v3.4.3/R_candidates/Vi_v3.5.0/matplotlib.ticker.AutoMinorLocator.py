class AutoMinorLocator(Locator):
    """
    Dynamically find minor tick positions based on the positions of
    major ticks. The scale must be linear with major ticks evenly spaced.
    """
    def __init__(self, n=None):
        """
        *n* is the number of subdivisions of the interval between
        major ticks; e.g., n=2 will place a single minor tick midway
        between major ticks.

        If *n* is omitted or None, it will be set to 5 or 4.
        """
        self.ndivs = n

    def __call__(self):
        """Return the locations of the ticks."""
        if self.axis.get_scale() == 'log':
            _api.warn_external('AutoMinorLocator does not work with '
                               'logarithmic scale')
            return []

        majorlocs = self.axis.get_majorticklocs()
        try:
            majorstep = majorlocs[1] - majorlocs[0]
        except IndexError:
            # Need at least two major ticks to find minor tick locations
            # TODO: Figure out a way to still be able to display minor
            # ticks without two major ticks visible. For now, just display
            # no ticks at all.
            return []

        if self.ndivs is None:

            majorstep_no_exponent = 10 ** (np.log10(majorstep) % 1)

            if np.isclose(majorstep_no_exponent, [1.0, 2.5, 5.0, 10.0]).any():
                ndivs = 5
            else:
                ndivs = 4
        else:
            ndivs = self.ndivs

        minorstep = majorstep / ndivs

        vmin, vmax = self.axis.get_view_interval()
        if vmin > vmax:
            vmin, vmax = vmax, vmin

        t0 = majorlocs[0]
        tmin = ((vmin - t0) // minorstep + 1) * minorstep
        tmax = ((vmax - t0) // minorstep + 1) * minorstep
        locs = np.arange(tmin, tmax, minorstep) + t0

        return self.raise_if_exceeds(locs)

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Cannot get tick locations for a '
                                  '%s type.' % type(self))

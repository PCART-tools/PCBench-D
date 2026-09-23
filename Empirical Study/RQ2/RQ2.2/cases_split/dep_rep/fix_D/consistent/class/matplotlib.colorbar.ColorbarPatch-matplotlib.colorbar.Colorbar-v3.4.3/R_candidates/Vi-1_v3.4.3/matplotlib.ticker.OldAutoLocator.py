@_api.deprecated("3.3")
class OldAutoLocator(Locator):
    """
    On autoscale this class picks the best MultipleLocator to set the
    view limits and the tick locs.
    """

    def __call__(self):
        # docstring inherited
        vmin, vmax = self.axis.get_view_interval()
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        d = abs(vmax - vmin)
        locator = self.get_locator(d)
        return self.raise_if_exceeds(locator())

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Cannot get tick locations for a '
                                  '%s type.' % type(self))

    def view_limits(self, vmin, vmax):
        # docstring inherited
        d = abs(vmax - vmin)
        locator = self.get_locator(d)
        return locator.view_limits(vmin, vmax)

    def get_locator(self, d):
        """Pick the best locator based on a distance *d*."""
        d = abs(d)
        if d <= 0:
            locator = MultipleLocator(0.2)
        else:

            try:
                ld = math.log10(d)
            except OverflowError as err:
                raise RuntimeError('AutoLocator illegal data interval '
                                   'range') from err

            fld = math.floor(ld)
            base = 10 ** fld

            #if ld==fld:  base = 10**(fld-1)
            #else:        base = 10**fld

            if d >= 5 * base:
                ticksize = base
            elif d >= 2 * base:
                ticksize = base / 2.0
            else:
                ticksize = base / 5.0
            locator = MultipleLocator(ticksize)

        return locator

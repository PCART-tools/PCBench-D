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

            if self.axis.axis_name == 'y':
                self.ndivs = mpl.rcParams['ytick.minor.ndivs']
            else:
                # for x and z axis
                self.ndivs = mpl.rcParams['xtick.minor.ndivs']

        if self.ndivs == 'auto':

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
        tmin = round((vmin - t0) / minorstep)
        tmax = round((vmax - t0) / minorstep) + 1
        locs = (np.arange(tmin, tmax) * minorstep) + t0

        return self.raise_if_exceeds(locs)

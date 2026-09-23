    def __call__(self):
        # docstring inherited
        if self.axis.get_scale() == 'log':
            _api.warn_external('AutoMinorLocator does not work on logarithmic scales')
            return []

        majorlocs = np.unique(self.axis.get_majorticklocs())
        if len(majorlocs) < 2:
            # Need at least two major ticks to find minor tick locations.
            # TODO: Figure out a way to still be able to display minor ticks with less
            # than two major ticks visible. For now, just display no ticks at all.
            return []
        majorstep = majorlocs[1] - majorlocs[0]

        if self.ndivs is None:
            self.ndivs = mpl.rcParams[
                'ytick.minor.ndivs' if self.axis.axis_name == 'y'
                else 'xtick.minor.ndivs']  # for x and z axis

        if self.ndivs == 'auto':
            majorstep_mantissa = 10 ** (np.log10(majorstep) % 1)
            ndivs = 5 if np.isclose(majorstep_mantissa, [1, 2.5, 5, 10]).any() else 4
        else:
            ndivs = self.ndivs

        minorstep = majorstep / ndivs

        vmin, vmax = sorted(self.axis.get_view_interval())
        t0 = majorlocs[0]
        tmin = round((vmin - t0) / minorstep)
        tmax = round((vmax - t0) / minorstep) + 1
        locs = (np.arange(tmin, tmax) * minorstep) + t0

        return self.raise_if_exceeds(locs)

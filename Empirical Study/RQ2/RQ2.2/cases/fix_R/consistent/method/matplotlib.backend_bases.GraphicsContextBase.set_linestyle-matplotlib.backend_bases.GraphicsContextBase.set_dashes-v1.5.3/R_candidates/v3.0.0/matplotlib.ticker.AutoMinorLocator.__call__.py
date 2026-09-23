    def __call__(self):
        'Return the locations of the ticks'
        if self.axis.get_scale() == 'log':
            warnings.warn('AutoMinorLocator does not work with logarithmic '
                          'scale')
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
            x = int(np.round(10 ** (np.log10(majorstep) % 1)))
            if x in [1, 5, 10]:
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
        mod = np.abs((locs - t0) % majorstep)
        cond1 = mod > minorstep / 10.0
        cond2 = ~np.isclose(mod, majorstep, atol=0)
        locs = locs.compress(cond1 & cond2)

        return self.raise_if_exceeds(np.array(locs))

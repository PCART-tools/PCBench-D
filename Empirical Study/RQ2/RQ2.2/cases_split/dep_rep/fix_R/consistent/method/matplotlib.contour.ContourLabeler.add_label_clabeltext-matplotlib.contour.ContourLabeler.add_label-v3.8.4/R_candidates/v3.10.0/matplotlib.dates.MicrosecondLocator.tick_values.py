    def tick_values(self, vmin, vmax):
        nmin, nmax = date2num((vmin, vmax))
        t0 = np.floor(nmin)
        nmax = nmax - t0
        nmin = nmin - t0
        nmin *= MUSECONDS_PER_DAY
        nmax *= MUSECONDS_PER_DAY

        ticks = self._wrapped_locator.tick_values(nmin, nmax)

        ticks = ticks / MUSECONDS_PER_DAY + t0
        return ticks

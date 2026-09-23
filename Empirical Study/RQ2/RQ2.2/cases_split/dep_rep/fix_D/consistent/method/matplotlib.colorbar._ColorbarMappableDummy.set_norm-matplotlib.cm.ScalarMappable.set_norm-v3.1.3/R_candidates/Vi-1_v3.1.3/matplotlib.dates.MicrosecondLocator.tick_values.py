    def tick_values(self, vmin, vmax):
        nmin, nmax = date2num((vmin, vmax))
        nmin *= MUSECONDS_PER_DAY
        nmax *= MUSECONDS_PER_DAY
        ticks = self._wrapped_locator.tick_values(nmin, nmax)
        ticks = [tick / MUSECONDS_PER_DAY for tick in ticks]
        return ticks

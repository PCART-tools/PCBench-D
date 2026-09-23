    def tick_values(self, vmin, vmax):
        """"
        Return the locations of the ticks.

        .. note::

            Because the values are fixed, vmin and vmax are not used in this
            method.

        """
        if self.nbins is None:
            return self.locs
        step = max(int(0.99 + len(self.locs) / float(self.nbins)), 1)
        ticks = self.locs[::step]
        for i in range(1, step):
            ticks1 = self.locs[i::step]
            if np.abs(ticks1).min() < np.abs(ticks).min():
                ticks = ticks1
        return self.raise_if_exceeds(ticks)

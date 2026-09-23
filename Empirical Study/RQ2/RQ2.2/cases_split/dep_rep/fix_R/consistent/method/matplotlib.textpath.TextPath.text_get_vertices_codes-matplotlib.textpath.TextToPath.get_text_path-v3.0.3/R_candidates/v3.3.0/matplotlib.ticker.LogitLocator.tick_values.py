    def tick_values(self, vmin, vmax):
        # dummy axis has no axes attribute
        if hasattr(self.axis, "axes") and self.axis.axes.name == "polar":
            raise NotImplementedError("Polar axis cannot be logit scaled yet")

        if self._nbins == "auto":
            if self.axis is not None:
                nbins = self.axis.get_tick_space()
                if nbins < 2:
                    nbins = 2
            else:
                nbins = 9
        else:
            nbins = self._nbins

        # We define ideal ticks with their index:
        # linscale: ... 1e-3 1e-2 1e-1 1/2 1-1e-1 1-1e-2 1-1e-3 ...
        # b-scale : ... -3   -2   -1   0   1      2      3      ...
        def ideal_ticks(x):
            return 10 ** x if x < 0 else 1 - (10 ** (-x)) if x > 0 else 1 / 2

        vmin, vmax = self.nonsingular(vmin, vmax)
        binf = int(
            np.floor(np.log10(vmin))
            if vmin < 0.5
            else 0
            if vmin < 0.9
            else -np.ceil(np.log10(1 - vmin))
        )
        bsup = int(
            np.ceil(np.log10(vmax))
            if vmax <= 0.5
            else 1
            if vmax <= 0.9
            else -np.floor(np.log10(1 - vmax))
        )
        numideal = bsup - binf - 1
        if numideal >= 2:
            # have 2 or more wanted ideal ticks, so use them as major ticks
            if numideal > nbins:
                # to many ideal ticks, subsampling ideals for major ticks, and
                # take others for minor ticks
                subsampling_factor = math.ceil(numideal / nbins)
                if self._minor:
                    ticklocs = [
                        ideal_ticks(b)
                        for b in range(binf, bsup + 1)
                        if (b % subsampling_factor) != 0
                    ]
                else:
                    ticklocs = [
                        ideal_ticks(b)
                        for b in range(binf, bsup + 1)
                        if (b % subsampling_factor) == 0
                    ]
                return self.raise_if_exceeds(np.array(ticklocs))
            if self._minor:
                ticklocs = []
                for b in range(binf, bsup):
                    if b < -1:
                        ticklocs.extend(np.arange(2, 10) * 10 ** b)
                    elif b == -1:
                        ticklocs.extend(np.arange(2, 5) / 10)
                    elif b == 0:
                        ticklocs.extend(np.arange(6, 9) / 10)
                    else:
                        ticklocs.extend(
                            1 - np.arange(2, 10)[::-1] * 10 ** (-b - 1)
                        )
                return self.raise_if_exceeds(np.array(ticklocs))
            ticklocs = [ideal_ticks(b) for b in range(binf, bsup + 1)]
            return self.raise_if_exceeds(np.array(ticklocs))
        # the scale is zoomed so same ticks as linear scale can be used
        if self._minor:
            return []
        return MaxNLocator.tick_values(self, vmin, vmax)

    def set_locs(self, locs=None):
        """
        Use axis view limits to control which ticks are labeled.

        The *locs* parameter is ignored in the present algorithm.

        """
        if np.isinf(self.minor_thresholds[0]):
            self._sublabels = None
            return

        # Handle symlog case:
        linthresh = self._linthresh
        if linthresh is None:
            try:
                linthresh = self.axis.get_transform().linthresh
            except AttributeError:
                pass

        vmin, vmax = self.axis.get_view_interval()
        if vmin > vmax:
            vmin, vmax = vmax, vmin

        if linthresh is None and vmin <= 0:
            # It's probably a colorbar with
            # a format kwarg setting a LogFormatter in the manner
            # that worked with 1.5.x, but that doesn't work now.
            self._sublabels = {1}  # label powers of base
            return

        b = self._base
        if linthresh is not None:  # symlog
            # Only compute the number of decades in the logarithmic part of the
            # axis
            numdec = 0
            if vmin < -linthresh:
                rhs = min(vmax, -linthresh)
                numdec += math.log(vmin / rhs) / math.log(b)
            if vmax > linthresh:
                lhs = max(vmin, linthresh)
                numdec += math.log(vmax / lhs) / math.log(b)
        else:
            vmin = math.log(vmin) / math.log(b)
            vmax = math.log(vmax) / math.log(b)
            numdec = abs(vmax - vmin)

        if numdec > self.minor_thresholds[0]:
            # Label only bases
            self._sublabels = {1}
        elif numdec > self.minor_thresholds[1]:
            # Add labels between bases at log-spaced coefficients;
            # include base powers in case the locations include
            # "major" and "minor" points, as in colorbar.
            c = np.logspace(0, 1, int(b)//2 + 1, base=b)
            self._sublabels = set(np.round(c))
            # For base 10, this yields (1, 2, 3, 4, 6, 10).
        else:
            # Label all integer multiples of base**n.
            self._sublabels = set(np.arange(1, b + 1))

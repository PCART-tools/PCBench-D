    def _process_levels(self):
        """
        Assign values to :attr:`layers` based on :attr:`levels`,
        adding extended layers as needed if contours are filled.

        For line contours, layers simply coincide with levels;
        a line is a thin layer.  No extended levels are needed
        with line contours.
        """
        # following are deprecated and will be removed in 2.2
        self._vmin = np.min(self.levels)
        self._vmax = np.max(self.levels)

        # Make a private _levels to include extended regions; we
        # want to leave the original levels attribute unchanged.
        # (Colorbar needs this even for line contours.)
        self._levels = list(self.levels)

        if self.extend in ('both', 'min'):
            self._levels.insert(0, min(self.levels[0], self.zmin) - 1)
        if self.extend in ('both', 'max'):
            self._levels.append(max(self.levels[-1], self.zmax) + 1)
        self._levels = np.asarray(self._levels)

        if not self.filled:
            self.layers = self.levels
            return

        # layer values are mid-way between levels
        self.layers = 0.5 * (self._levels[:-1] + self._levels[1:])
        # ...except that extended layers must be outside the
        # normed range:
        if self.extend in ('both', 'min'):
            self.layers[0] = -1e150
        if self.extend in ('both', 'max'):
            self.layers[-1] = 1e150

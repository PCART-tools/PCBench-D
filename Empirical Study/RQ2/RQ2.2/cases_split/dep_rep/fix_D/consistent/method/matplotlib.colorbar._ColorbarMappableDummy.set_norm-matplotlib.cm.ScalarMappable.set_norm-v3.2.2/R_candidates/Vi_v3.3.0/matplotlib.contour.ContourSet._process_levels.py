    def _process_levels(self):
        """
        Assign values to :attr:`layers` based on :attr:`levels`,
        adding extended layers as needed if contours are filled.

        For line contours, layers simply coincide with levels;
        a line is a thin layer.  No extended levels are needed
        with line contours.
        """
        # Make a private _levels to include extended regions; we
        # want to leave the original levels attribute unchanged.
        # (Colorbar needs this even for line contours.)
        self._levels = list(self.levels)

        if self.logscale:
            lower, upper = 1e-250, 1e250
        else:
            lower, upper = -1e250, 1e250

        if self.extend in ('both', 'min'):
            self._levels.insert(0, lower)
        if self.extend in ('both', 'max'):
            self._levels.append(upper)
        self._levels = np.asarray(self._levels)

        if not self.filled:
            self.layers = self.levels
            return

        # Layer values are mid-way between levels in screen space.
        if self.logscale:
            # Avoid overflow by taking sqrt before multiplying.
            self.layers = (np.sqrt(self._levels[:-1])
                           * np.sqrt(self._levels[1:]))
        else:
            self.layers = 0.5 * (self._levels[:-1] + self._levels[1:])

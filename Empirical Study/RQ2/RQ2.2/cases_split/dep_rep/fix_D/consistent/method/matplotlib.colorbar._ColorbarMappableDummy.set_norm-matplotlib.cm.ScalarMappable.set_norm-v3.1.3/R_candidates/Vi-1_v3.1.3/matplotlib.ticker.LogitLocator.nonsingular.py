    def nonsingular(self, vmin, vmax):
        initial_range = (1e-7, 1 - 1e-7)
        if not np.isfinite(vmin) or not np.isfinite(vmax):
            return initial_range  # no data plotted yet

        if vmin > vmax:
            vmin, vmax = vmax, vmin

        # what to do if a window beyond ]0, 1[ is chosen
        if self.axis is not None:
            minpos = self.axis.get_minpos()
            if not np.isfinite(minpos):
                return initial_range  # again, no data plotted
        else:
            minpos = 1e-7  # should not occur in normal use

        # NOTE: for vmax, we should query a property similar to get_minpos, but
        # related to the maximal, less-than-one data point. Unfortunately,
        # Bbox._minpos is defined very deep in the BBox and updated with data,
        # so for now we use 1 - minpos as a substitute.

        if vmin <= 0:
            vmin = minpos
        if vmax >= 1:
            vmax = 1 - minpos
        if vmin == vmax:
            return 0.1 * vmin, 1 - 0.1 * vmin

        return vmin, vmax

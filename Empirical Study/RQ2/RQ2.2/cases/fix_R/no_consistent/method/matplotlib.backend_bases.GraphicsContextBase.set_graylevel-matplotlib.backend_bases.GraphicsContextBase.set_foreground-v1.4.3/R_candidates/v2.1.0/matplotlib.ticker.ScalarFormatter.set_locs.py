    def set_locs(self, locs):
        """
        Set the locations of the ticks.
        """
        self.locs = locs
        if len(self.locs) > 0:
            vmin, vmax = self.axis.get_view_interval()
            d = abs(vmax - vmin)
            if self._useOffset:
                self._compute_offset()
            self._set_orderOfMagnitude(d)
            self._set_format(vmin, vmax)

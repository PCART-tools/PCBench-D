    def set_locs(self, locs):
        """
        Set the locations of the ticks.
        """
        self.locs = locs
        if len(self.locs) > 0:
            if self._useOffset:
                self._compute_offset()
            self._set_order_of_magnitude()
            self._set_format()

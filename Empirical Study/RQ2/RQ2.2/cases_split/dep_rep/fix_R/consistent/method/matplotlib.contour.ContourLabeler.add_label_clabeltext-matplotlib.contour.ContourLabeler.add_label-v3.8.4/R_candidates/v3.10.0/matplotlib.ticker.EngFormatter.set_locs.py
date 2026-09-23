    def set_locs(self, locs):
        # docstring inherited
        self.locs = locs
        if len(self.locs) > 0:
            vmin, vmax = sorted(self.axis.get_view_interval())
            if self._useOffset:
                self._compute_offset()
                if self.offset != 0:
                    # We don't want to use the offset computed by
                    # self._compute_offset because it rounds the offset unaware
                    # of our engineering prefixes preference, and this can
                    # cause ticks with 4+ digits to appear. These ticks are
                    # slightly less readable, so if offset is justified
                    # (decided by self._compute_offset) we set it to better
                    # value:
                    self.offset = round((vmin + vmax)/2, 3)
            # Use log1000 to use engineers' oom standards
            self.orderOfMagnitude = math.floor(math.log(vmax - vmin, 1000))*3
            self._set_format()

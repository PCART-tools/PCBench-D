    def _compute_offset(self):
        locs = self.locs
        # Restrict to visible ticks.
        vmin, vmax = sorted(self.axis.get_view_interval())
        locs = np.asarray(locs)
        locs = locs[(vmin <= locs) & (locs <= vmax)]
        if not len(locs):
            self.offset = 0
            return
        lmin, lmax = locs.min(), locs.max()
        # Only use offset if there are at least two ticks and every tick has
        # the same sign.
        if lmin == lmax or lmin <= 0 <= lmax:
            self.offset = 0
            return
        # min, max comparing absolute values (we want division to round towards
        # zero so we work on absolute values).
        abs_min, abs_max = sorted([abs(float(lmin)), abs(float(lmax))])
        sign = math.copysign(1, lmin)
        # What is the smallest power of ten such that abs_min and abs_max are
        # equal up to that precision?
        # Note: Internally using oom instead of 10 ** oom avoids some numerical
        # accuracy issues.
        oom_max = np.ceil(math.log10(abs_max))
        oom = 1 + next(oom for oom in itertools.count(oom_max, -1)
                       if abs_min // 10 ** oom != abs_max // 10 ** oom)
        if (abs_max - abs_min) / 10 ** oom <= 1e-2:
            # Handle the case of straddling a multiple of a large power of ten
            # (relative to the span).
            # What is the smallest power of ten such that abs_min and abs_max
            # are no more than 1 apart at that precision?
            oom = 1 + next(oom for oom in itertools.count(oom_max, -1)
                           if abs_max // 10 ** oom - abs_min // 10 ** oom > 1)
        # Only use offset if it saves at least _offset_threshold digits.
        n = self._offset_threshold - 1
        self.offset = (sign * (abs_max // 10 ** oom) * 10 ** oom
                       if abs_max // 10 ** oom >= 10**n
                       else 0)

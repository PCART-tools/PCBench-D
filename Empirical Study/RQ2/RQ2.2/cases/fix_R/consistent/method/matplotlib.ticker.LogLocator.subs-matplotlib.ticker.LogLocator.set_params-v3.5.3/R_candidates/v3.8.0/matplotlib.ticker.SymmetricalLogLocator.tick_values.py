    def tick_values(self, vmin, vmax):
        linthresh = self._linthresh

        if vmax < vmin:
            vmin, vmax = vmax, vmin

        # The domain is divided into three sections, only some of
        # which may actually be present.
        #
        # <======== -t ==0== t ========>
        # aaaaaaaaa    bbbbb   ccccccccc
        #
        # a) and c) will have ticks at integral log positions.  The
        # number of ticks needs to be reduced if there are more
        # than self.numticks of them.
        #
        # b) has a tick at 0 and only 0 (we assume t is a small
        # number, and the linear segment is just an implementation
        # detail and not interesting.)
        #
        # We could also add ticks at t, but that seems to usually be
        # uninteresting.
        #
        # "simple" mode is when the range falls entirely within [-t, t]
        #  -- it should just display (vmin, 0, vmax)
        if -linthresh <= vmin < vmax <= linthresh:
            # only the linear range is present
            return sorted({vmin, 0, vmax})

        # Lower log range is present
        has_a = (vmin < -linthresh)
        # Upper log range is present
        has_c = (vmax > linthresh)

        # Check if linear range is present
        has_b = (has_a and vmax > -linthresh) or (has_c and vmin < linthresh)

        base = self._base

        def get_log_range(lo, hi):
            lo = np.floor(np.log(lo) / np.log(base))
            hi = np.ceil(np.log(hi) / np.log(base))
            return lo, hi

        # Calculate all the ranges, so we can determine striding
        a_lo, a_hi = (0, 0)
        if has_a:
            a_upper_lim = min(-linthresh, vmax)
            a_lo, a_hi = get_log_range(abs(a_upper_lim), abs(vmin) + 1)

        c_lo, c_hi = (0, 0)
        if has_c:
            c_lower_lim = max(linthresh, vmin)
            c_lo, c_hi = get_log_range(c_lower_lim, vmax + 1)

        # Calculate the total number of integer exponents in a and c ranges
        total_ticks = (a_hi - a_lo) + (c_hi - c_lo)
        if has_b:
            total_ticks += 1
        stride = max(total_ticks // (self.numticks - 1), 1)

        decades = []
        if has_a:
            decades.extend(-1 * (base ** (np.arange(a_lo, a_hi,
                                                    stride)[::-1])))

        if has_b:
            decades.append(0.0)

        if has_c:
            decades.extend(base ** (np.arange(c_lo, c_hi, stride)))

        subs = np.asarray(self._subs)

        if len(subs) > 1 or subs[0] != 1.0:
            ticklocs = []
            for decade in decades:
                if decade == 0:
                    ticklocs.append(decade)
                else:
                    ticklocs.extend(subs * decade)
        else:
            ticklocs = decades

        return self.raise_if_exceeds(np.array(ticklocs))

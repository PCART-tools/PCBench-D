    def _update_ticks(self, renderer):
        """
        Update ticks (position and labels) using the current data
        interval of the axes. Returns a list of ticks that will be
        drawn.
        """

        interval = self.get_view_interval()
        tick_tups = list(self.iter_ticks())  # iter_ticks calls the locator
        if self._smart_bounds and tick_tups:
            # handle inverted limits
            view_low, view_high = sorted(interval)
            data_low, data_high = sorted(self.get_data_interval())
            locs = np.sort([ti[1] for ti in tick_tups])
            if data_low <= view_low:
                # data extends beyond view, take view as limit
                ilow = view_low
            else:
                # data stops within view, take best tick
                good_locs = locs[locs <= data_low]
                if len(good_locs):
                    # last tick prior or equal to first data point
                    ilow = good_locs[-1]
                else:
                    # No ticks (why not?), take first tick
                    ilow = locs[0]
            if data_high >= view_high:
                # data extends beyond view, take view as limit
                ihigh = view_high
            else:
                # data stops within view, take best tick
                good_locs = locs[locs >= data_high]
                if len(good_locs):
                    # first tick after or equal to last data point
                    ihigh = good_locs[0]
                else:
                    # No ticks (why not?), take last tick
                    ihigh = locs[-1]
            tick_tups = [ti for ti in tick_tups if ilow <= ti[1] <= ihigh]

        # so that we don't lose ticks on the end, expand out the interval ever
        # so slightly.  The "ever so slightly" is defined to be the width of a
        # half of a pixel.  We don't want to draw a tick that even one pixel
        # outside of the defined axis interval.
        if interval[0] <= interval[1]:
            interval_expanded = interval
        else:
            interval_expanded = interval[1], interval[0]

        if hasattr(self, '_get_pixel_distance_along_axis'):
            # normally, one does not want to catch all exceptions that
            # could possibly happen, but it is not clear exactly what
            # exceptions might arise from a user's projection (their
            # rendition of the Axis object).  So, we catch all, with
            # the idea that one would rather potentially lose a tick
            # from one side of the axis or another, rather than see a
            # stack trace.
            # We also catch users warnings here. These are the result of
            # invalid numpy calculations that may be the result of out of
            # bounds on axis with finite allowed intervals such as geo
            # projections i.e. Mollweide.
            with np.errstate(invalid='ignore'):
                try:
                    ds1 = self._get_pixel_distance_along_axis(
                        interval_expanded[0], -0.5)
                except:
                    warnings.warn("Unable to find pixel distance along axis "
                                  "for interval padding of ticks; assuming no "
                                  "interval padding needed.")
                    ds1 = 0.0
                if np.isnan(ds1):
                    ds1 = 0.0
                try:
                    ds2 = self._get_pixel_distance_along_axis(
                        interval_expanded[1], +0.5)
                except:
                    warnings.warn("Unable to find pixel distance along axis "
                                  "for interval padding of ticks; assuming no "
                                  "interval padding needed.")
                    ds2 = 0.0
                if np.isnan(ds2):
                    ds2 = 0.0
            interval_expanded = (interval_expanded[0] - ds1,
                                 interval_expanded[1] + ds2)

        ticks_to_draw = []
        for tick, loc, label in tick_tups:
            if tick is None:
                continue
            # NB: always update labels and position to avoid issues like #9397
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
            if not mtransforms.interval_contains(interval_expanded, loc):
                continue
            ticks_to_draw.append(tick)

        return ticks_to_draw

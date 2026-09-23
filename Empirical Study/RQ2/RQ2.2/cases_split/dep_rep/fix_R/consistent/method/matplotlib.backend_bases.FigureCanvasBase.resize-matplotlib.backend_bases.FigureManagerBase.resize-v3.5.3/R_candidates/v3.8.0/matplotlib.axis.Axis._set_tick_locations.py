    def _set_tick_locations(self, ticks, *, minor=False):
        # see docstring of set_ticks

        # XXX if the user changes units, the information will be lost here
        ticks = self.convert_units(ticks)
        locator = mticker.FixedLocator(ticks)  # validate ticks early.
        if len(ticks):
            for axis in self._get_shared_axis():
                # set_view_interval maintains any preexisting inversion.
                axis.set_view_interval(min(ticks), max(ticks))
        self.axes.stale = True
        if minor:
            self.set_minor_locator(locator)
            return self.get_minor_ticks(len(ticks))
        else:
            self.set_major_locator(locator)
            return self.get_major_ticks(len(ticks))

    def _set_tick_locations(self, ticks, *, minor=False):
        # see docstring of set_ticks

        # XXX if the user changes units, the information will be lost here
        ticks = self.convert_units(ticks)
        for name, axis in self.axes._axis_map.items():
            if self is axis:
                shared = [
                    getattr(ax, f"{name}axis")
                    for ax
                    in self.axes._shared_axes[name].get_siblings(self.axes)]
                break
        else:
            shared = [self]
        if len(ticks):
            for axis in shared:
                # set_view_interval maintains any preexisting inversion.
                axis.set_view_interval(min(ticks), max(ticks))
        self.axes.stale = True
        if minor:
            self.set_minor_locator(mticker.FixedLocator(ticks))
            return self.get_minor_ticks(len(ticks))
        else:
            self.set_major_locator(mticker.FixedLocator(ticks))
            return self.get_major_ticks(len(ticks))

    @cbook._make_keyword_only("3.2", "minor")
    def set_ticks(self, ticks, minor=False):
        """
        Set this Axis' tick locations.

        Parameters
        ----------
        ticks : list of floats
            List of tick locations.
        minor : bool, default: False
            If ``False``, set the major ticks; if ``True``, the minor ticks.
        """
        # XXX if the user changes units, the information will be lost here
        ticks = self.convert_units(ticks)
        if len(ticks) > 1:
            xleft, xright = self.get_view_interval()
            if xright > xleft:
                self.set_view_interval(min(ticks), max(ticks))
            else:
                self.set_view_interval(max(ticks), min(ticks))
        self.axes.stale = True
        if minor:
            self.set_minor_locator(mticker.FixedLocator(ticks))
            return self.get_minor_ticks(len(ticks))
        else:
            self.set_major_locator(mticker.FixedLocator(ticks))
            return self.get_major_ticks(len(ticks))

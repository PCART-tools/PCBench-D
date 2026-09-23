    @cbook._make_keyword_only("3.2", "minor")
    def set_ticks(self, ticks, minor=False):
        """
        Set the x ticks with list of *ticks*

        Parameters
        ----------
        ticks : list
            List of x-axis tick locations.
        minor : bool, default: False
            If ``False`` sets major ticks, if ``True`` sets minor ticks.
        """
        ret = self._axis.set_ticks(ticks, minor=minor)
        self.stale = True
        self._ticks_set = True
        return ret

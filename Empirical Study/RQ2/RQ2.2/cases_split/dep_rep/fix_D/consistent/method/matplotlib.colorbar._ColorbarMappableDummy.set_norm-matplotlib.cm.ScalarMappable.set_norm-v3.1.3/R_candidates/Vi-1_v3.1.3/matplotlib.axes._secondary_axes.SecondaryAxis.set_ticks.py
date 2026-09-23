    def set_ticks(self, ticks, minor=False):
        """
        Set the x ticks with list of *ticks*

        Parameters
        ----------
        ticks : list
            List of x-axis tick locations.

        minor : bool, optional
            If ``False`` sets major ticks, if ``True`` sets minor ticks.
            Default is ``False``.
        """
        ret = self._axis.set_ticks(ticks, minor=minor)
        self.stale = True
        self._ticks_set = True
        return ret

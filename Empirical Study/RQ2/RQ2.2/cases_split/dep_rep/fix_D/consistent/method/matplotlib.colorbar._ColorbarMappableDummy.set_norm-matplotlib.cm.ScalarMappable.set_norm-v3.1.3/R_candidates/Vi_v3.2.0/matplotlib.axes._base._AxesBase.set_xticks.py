    @cbook._make_keyword_only("3.2", "minor")
    def set_xticks(self, ticks, minor=False):
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
        ret = self.xaxis.set_ticks(ticks, minor=minor)
        self.stale = True
        return ret

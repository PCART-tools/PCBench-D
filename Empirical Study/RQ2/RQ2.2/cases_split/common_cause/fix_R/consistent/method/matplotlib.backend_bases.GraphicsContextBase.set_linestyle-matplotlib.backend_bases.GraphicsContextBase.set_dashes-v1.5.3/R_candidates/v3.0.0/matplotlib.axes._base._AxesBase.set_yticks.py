    def set_yticks(self, ticks, minor=False):
        """
        Set the y ticks with list of *ticks*

        Parameters
        ----------
        ticks : list
            List of y-axis tick locations

        minor : bool, optional
            If ``False`` sets major ticks, if ``True`` sets minor ticks.
            Default is ``False``.
        """
        ret = self.yaxis.set_ticks(ticks, minor=minor)
        return ret

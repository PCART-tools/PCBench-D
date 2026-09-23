
    def mask(self, cond):
        """
        Returns copy of self whose values are replaced with nan if the
        inverted condition is True

        Parameters
        ----------
        cond: boolean Series or array

        Returns
        -------
        wh: Series
        """
        return self.where(~cond, nan)

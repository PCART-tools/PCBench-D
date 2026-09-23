
    def mask(self, cond):
        """
        Returns copy of self whose values are replaced with nan if the
        inverted condition is True

        Parameters
        ----------
        cond: boolean DataFrame or array

        Returns
        -------
        wh: DataFrame
        """
        return self.where(~cond, NA)

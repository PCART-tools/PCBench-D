    def mask(self, cond):
        """
        Returns copy whose values are replaced with nan if the
        inverted condition is True

        Parameters
        ----------
        cond : boolean NDFrame or array

        Returns
        -------
        wh: same as input
        """
        return self.where(~cond, np.nan)

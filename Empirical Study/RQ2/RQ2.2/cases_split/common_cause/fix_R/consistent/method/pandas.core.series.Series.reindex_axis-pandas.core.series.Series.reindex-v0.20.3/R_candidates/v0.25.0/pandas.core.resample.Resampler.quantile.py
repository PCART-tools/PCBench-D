    def quantile(self, q=0.5, **kwargs):
        """
        Return value at the given quantile.

        .. versionadded:: 0.24.0

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)

        Returns
        -------
        DataFrame or Series
            Quantile of values within each group.

        See Also
        --------
        Series.quantile
        DataFrame.quantile
        DataFrameGroupBy.quantile
        """
        return self._downsample("quantile", q=q, **kwargs)

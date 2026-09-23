    def quantile(self, q=0.5):
        """
        Return value at the given quantile, a la numpy.percentile.

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)
            0 <= q <= 1, the quantile(s) to compute

        Returns
        -------
        quantile : float or Series
            if ``q`` is an array, a Series will be returned where the
            index is ``q`` and the values are the quantiles.

        Examples
        --------

        >>> s = Series([1, 2, 3, 4])
        >>> s.quantile(.5)
            2.5
        >>> s.quantile([.25, .5, .75])
        0.25    1.75
        0.50    2.50
        0.75    3.25
        dtype: float64
        """
        valid = self.dropna()

        def multi(values, qs):
            if com.is_list_like(qs):
                return Series([_quantile(values, x*100)
                               for x in qs], index=qs)
            else:
                return _quantile(values, qs*100)

        return self._maybe_box(lambda values: multi(values, q), dropna=True)

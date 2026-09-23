    def quantile(self, q=0.5, interpolation='linear'):
        """
        Return value at the given quantile, a la numpy.percentile.

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)
            0 <= q <= 1, the quantile(s) to compute
        interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
            .. versionadded:: 0.18.0

            This optional parameter specifies the interpolation method to use,
            when the desired quantile lies between two data points `i` and `j`:

                * linear: `i + (j - i) * fraction`, where `fraction` is the
                  fractional part of the index surrounded by `i` and `j`.
                * lower: `i`.
                * higher: `j`.
                * nearest: `i` or `j` whichever is nearest.
                * midpoint: (`i` + `j`) / 2.

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

        See Also
        --------
        pandas.core.window.Rolling.quantile
        """

        self._check_percentile(q)

        result = self._data.quantile(qs=q, interpolation=interpolation)

        if is_list_like(q):
            return self._constructor(result,
                                     index=Float64Index(q),
                                     name=self.name)
        else:
            # scalar
            return result

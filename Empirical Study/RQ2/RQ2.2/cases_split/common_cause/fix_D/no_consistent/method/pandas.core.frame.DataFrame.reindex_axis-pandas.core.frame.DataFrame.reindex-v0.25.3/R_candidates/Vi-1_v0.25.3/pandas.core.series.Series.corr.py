    def corr(self, other, method="pearson", min_periods=None):
        """
        Compute correlation with `other` Series, excluding missing values.

        Parameters
        ----------
        other : Series
            Series with which to compute the correlation.
        method : {'pearson', 'kendall', 'spearman'} or callable
            * pearson : standard correlation coefficient
            * kendall : Kendall Tau correlation coefficient
            * spearman : Spearman rank correlation
            * callable: callable with input two 1d ndarrays
                and returning a float. Note that the returned matrix from corr
                will have 1 along the diagonals and will be symmetric
                regardless of the callable's behavior
                .. versionadded:: 0.24.0

        min_periods : int, optional
            Minimum number of observations needed to have a valid result.

        Returns
        -------
        float
            Correlation with other.

        Examples
        --------
        >>> def histogram_intersection(a, b):
        ...     v = np.minimum(a, b).sum().round(decimals=1)
        ...     return v
        >>> s1 = pd.Series([.2, .0, .6, .2])
        >>> s2 = pd.Series([.3, .6, .0, .1])
        >>> s1.corr(s2, method=histogram_intersection)
        0.3
        """
        this, other = self.align(other, join="inner", copy=False)
        if len(this) == 0:
            return np.nan

        if method in ["pearson", "spearman", "kendall"] or callable(method):
            return nanops.nancorr(
                this.values, other.values, method=method, min_periods=min_periods
            )

        raise ValueError(
            "method must be either 'pearson', "
            "'spearman', 'kendall', or a callable, "
            "'{method}' was supplied".format(method=method)
        )

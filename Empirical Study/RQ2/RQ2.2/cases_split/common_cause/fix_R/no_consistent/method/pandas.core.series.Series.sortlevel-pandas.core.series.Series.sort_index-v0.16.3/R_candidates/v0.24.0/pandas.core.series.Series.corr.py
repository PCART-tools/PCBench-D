    def corr(self, other, method='pearson', min_periods=None):
        """
        Compute correlation with `other` Series, excluding missing values.

        Parameters
        ----------
        other : Series
        method : {'pearson', 'kendall', 'spearman'} or callable
            * pearson : standard correlation coefficient
            * kendall : Kendall Tau correlation coefficient
            * spearman : Spearman rank correlation
            * callable: callable with input two 1d ndarray
                and returning a float
                .. versionadded:: 0.24.0

        min_periods : int, optional
            Minimum number of observations needed to have a valid result

        Returns
        -------
        correlation : float

        Examples
        --------
        >>> histogram_intersection = lambda a, b: np.minimum(a, b
        ... ).sum().round(decimals=1)
        >>> s1 = pd.Series([.2, .0, .6, .2])
        >>> s2 = pd.Series([.3, .6, .0, .1])
        >>> s1.corr(s2, method=histogram_intersection)
        0.3
        """
        this, other = self.align(other, join='inner', copy=False)
        if len(this) == 0:
            return np.nan

        if method in ['pearson', 'spearman', 'kendall'] or callable(method):
            return nanops.nancorr(this.values, other.values, method=method,
                                  min_periods=min_periods)

        raise ValueError("method must be either 'pearson', "
                         "'spearman', or 'kendall', '{method}' "
                         "was supplied".format(method=method))

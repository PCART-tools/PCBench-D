    def cov(self, other, min_periods=None):
        """
        Compute covariance with Series, excluding missing values.

        Parameters
        ----------
        other : Series
            Series with which to compute the covariance.
        min_periods : int, optional
            Minimum number of observations needed to have a valid result.

        Returns
        -------
        float
            Covariance between Series and other normalized by N-1
            (unbiased estimator).

        Examples
        --------
        >>> s1 = pd.Series([0.90010907, 0.13484424, 0.62036035])
        >>> s2 = pd.Series([0.12528585, 0.26962463, 0.51111198])
        >>> s1.cov(s2)
        -0.01685762652715874
        """
        this, other = self.align(other, join="inner", copy=False)
        if len(this) == 0:
            return np.nan
        return nanops.nancov(this.values, other.values, min_periods=min_periods)

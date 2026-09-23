    def cov(self, other, min_periods=None):
        """
        Compute covariance with Series, excluding missing values.

        Parameters
        ----------
        other : Series
        min_periods : int, optional
            Minimum number of observations needed to have a valid result

        Returns
        -------
        covariance : float

        Normalized by N-1 (unbiased estimator).
        """
        this, other = self.align(other, join='inner', copy=False)
        if len(this) == 0:
            return np.nan
        return nanops.nancov(this.values, other.values,
                             min_periods=min_periods)

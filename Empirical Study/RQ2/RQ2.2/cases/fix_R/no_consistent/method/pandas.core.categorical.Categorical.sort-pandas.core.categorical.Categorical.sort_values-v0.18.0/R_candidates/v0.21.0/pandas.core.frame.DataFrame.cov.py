    def cov(self, min_periods=None):
        """
        Compute pairwise covariance of columns, excluding NA/null values

        Parameters
        ----------
        min_periods : int, optional
            Minimum number of observations required per pair of columns
            to have a valid result.

        Returns
        -------
        y : DataFrame

        Notes
        -----
        `y` contains the covariance matrix of the DataFrame's time series.
        The covariance is normalized by N-1 (unbiased estimator).
        """
        numeric_df = self._get_numeric_data()
        cols = numeric_df.columns
        idx = cols.copy()
        mat = numeric_df.values

        if notna(mat).all():
            if min_periods is not None and min_periods > len(mat):
                baseCov = np.empty((mat.shape[1], mat.shape[1]))
                baseCov.fill(np.nan)
            else:
                baseCov = np.cov(mat.T)
            baseCov = baseCov.reshape((len(cols), len(cols)))
        else:
            baseCov = libalgos.nancorr(_ensure_float64(mat), cov=True,
                                       minp=min_periods)

        return self._constructor(baseCov, index=idx, columns=cols)

    def corr(self, method='pearson', min_periods=1):
        """
        Compute pairwise correlation of columns, excluding NA/null values

        Parameters
        ----------
        method : {'pearson', 'kendall', 'spearman'}
            * pearson : standard correlation coefficient
            * kendall : Kendall Tau correlation coefficient
            * spearman : Spearman rank correlation
        min_periods : int, optional
            Minimum number of observations required per pair of columns
            to have a valid result. Currently only available for pearson
            and spearman correlation

        Returns
        -------
        y : DataFrame
        """
        numeric_df = self._get_numeric_data()
        cols = numeric_df.columns
        idx = cols.copy()
        mat = numeric_df.values

        if method == 'pearson':
            correl = libalgos.nancorr(_ensure_float64(mat), minp=min_periods)
        elif method == 'spearman':
            correl = libalgos.nancorr_spearman(_ensure_float64(mat),
                                               minp=min_periods)
        else:
            if min_periods is None:
                min_periods = 1
            mat = _ensure_float64(mat).T
            corrf = nanops.get_corr_func(method)
            K = len(cols)
            correl = np.empty((K, K), dtype=float)
            mask = np.isfinite(mat)
            for i, ac in enumerate(mat):
                for j, bc in enumerate(mat):
                    if i > j:
                        continue

                    valid = mask[i] & mask[j]
                    if valid.sum() < min_periods:
                        c = np.nan
                    elif i == j:
                        c = 1.
                    elif not valid.all():
                        c = corrf(ac[valid], bc[valid])
                    else:
                        c = corrf(ac, bc)
                    correl[i, j] = c
                    correl[j, i] = c

        return self._constructor(correl, index=idx, columns=cols)

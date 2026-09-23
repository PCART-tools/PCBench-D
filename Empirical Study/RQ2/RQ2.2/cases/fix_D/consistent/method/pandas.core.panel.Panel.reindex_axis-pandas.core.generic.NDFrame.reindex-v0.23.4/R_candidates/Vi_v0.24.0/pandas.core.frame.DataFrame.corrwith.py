    def corrwith(self, other, axis=0, drop=False, method='pearson'):
        """
        Compute pairwise correlation between rows or columns of DataFrame
        with rows or columns of Series or DataFrame.  DataFrames are first
        aligned along both axes before computing the correlations.

        Parameters
        ----------
        other : DataFrame, Series
        axis : {0 or 'index', 1 or 'columns'}, default 0
            0 or 'index' to compute column-wise, 1 or 'columns' for row-wise
        drop : boolean, default False
            Drop missing indices from result
        method : {'pearson', 'kendall', 'spearman'} or callable
            * pearson : standard correlation coefficient
            * kendall : Kendall Tau correlation coefficient
            * spearman : Spearman rank correlation
            * callable: callable with input two 1d ndarrays
                and returning a float

            .. versionadded:: 0.24.0

        Returns
        -------
        correls : Series

        See Also
        -------
        DataFrame.corr
        """
        axis = self._get_axis_number(axis)
        this = self._get_numeric_data()

        if isinstance(other, Series):
            return this.apply(lambda x: other.corr(x, method=method),
                              axis=axis)

        other = other._get_numeric_data()
        left, right = this.align(other, join='inner', copy=False)

        if axis == 1:
            left = left.T
            right = right.T

        if method == 'pearson':
            # mask missing values
            left = left + right * 0
            right = right + left * 0

            # demeaned data
            ldem = left - left.mean()
            rdem = right - right.mean()

            num = (ldem * rdem).sum()
            dom = (left.count() - 1) * left.std() * right.std()

            correl = num / dom

        elif method in ['kendall', 'spearman'] or callable(method):
            def c(x):
                return nanops.nancorr(x[0], x[1], method=method)

            correl = Series(map(c,
                                zip(left.values.T, right.values.T)),
                            index=left.columns)

        else:
            raise ValueError("Invalid method {method} was passed, "
                             "valid methods are: 'pearson', 'kendall', "
                             "'spearman', or callable".
                             format(method=method))

        if not drop:
            # Find non-matching labels along the given axis
            # and append missing correlations (GH 22375)
            raxis = 1 if axis == 0 else 0
            result_index = (this._get_axis(raxis).
                            union(other._get_axis(raxis)))
            idx_diff = result_index.difference(correl.index)

            if len(idx_diff) > 0:
                correl = correl.append(Series([np.nan] * len(idx_diff),
                                              index=idx_diff))

        return correl

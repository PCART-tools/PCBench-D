    def corrwith(
        self,
        other: DataFrame | Series,
        axis: Axis = 0,
        drop: bool = False,
        method: CorrelationMethod = "pearson",
        numeric_only: bool = False,
    ) -> Series:
        """
        Compute pairwise correlation.

        Pairwise correlation is computed between rows or columns of
        DataFrame with rows or columns of Series or DataFrame. DataFrames
        are first aligned along both axes before computing the
        correlations.

        Parameters
        ----------
        other : DataFrame, Series
            Object with which to compute correlations.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            The axis to use. 0 or 'index' to compute row-wise, 1 or 'columns' for
            column-wise.
        drop : bool, default False
            Drop missing indices from result.
        method : {'pearson', 'kendall', 'spearman'} or callable
            Method of correlation:

            * pearson : standard correlation coefficient
            * kendall : Kendall Tau correlation coefficient
            * spearman : Spearman rank correlation
            * callable: callable with input two 1d ndarrays
                and returning a float.

        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

            .. versionadded:: 1.5.0

            .. versionchanged:: 2.0.0
                The default value of ``numeric_only`` is now ``False``.

        Returns
        -------
        Series
            Pairwise correlations.

        See Also
        --------
        DataFrame.corr : Compute pairwise correlation of columns.

        Examples
        --------
        >>> index = ["a", "b", "c", "d", "e"]
        >>> columns = ["one", "two", "three", "four"]
        >>> df1 = pd.DataFrame(np.arange(20).reshape(5, 4), index=index, columns=columns)
        >>> df2 = pd.DataFrame(np.arange(16).reshape(4, 4), index=index[:4], columns=columns)
        >>> df1.corrwith(df2)
        one      1.0
        two      1.0
        three    1.0
        four     1.0
        dtype: float64

        >>> df2.corrwith(df1, axis=1)
        a    1.0
        b    1.0
        c    1.0
        d    1.0
        e    NaN
        dtype: float64
        """  # noqa:E501
        axis = self._get_axis_number(axis)
        this = self._get_numeric_data() if numeric_only else self

        if isinstance(other, Series):
            return this.apply(lambda x: other.corr(x, method=method), axis=axis)

        if numeric_only:
            other = other._get_numeric_data()
        left, right = this.align(other, join="inner", copy=False)

        if axis == 1:
            left = left.T
            right = right.T

        if method == "pearson":
            # mask missing values
            left = left + right * 0
            right = right + left * 0

            # demeaned data
            ldem = left - left.mean(numeric_only=numeric_only)
            rdem = right - right.mean(numeric_only=numeric_only)

            num = (ldem * rdem).sum()
            dom = (
                (left.count() - 1)
                * left.std(numeric_only=numeric_only)
                * right.std(numeric_only=numeric_only)
            )

            correl = num / dom

        elif method in ["kendall", "spearman"] or callable(method):

            def c(x):
                return nanops.nancorr(x[0], x[1], method=method)

            correl = self._constructor_sliced(
                map(c, zip(left.values.T, right.values.T)),
                index=left.columns,
                copy=False,
            )

        else:
            raise ValueError(
                f"Invalid method {method} was passed, "
                "valid methods are: 'pearson', 'kendall', "
                "'spearman', or callable"
            )

        if not drop:
            # Find non-matching labels along the given axis
            # and append missing correlations (GH 22375)
            raxis: AxisInt = 1 if axis == 0 else 0
            result_index = this._get_axis(raxis).union(other._get_axis(raxis))
            idx_diff = result_index.difference(correl.index)

            if len(idx_diff) > 0:
                correl = correl._append(
                    Series([np.nan] * len(idx_diff), index=idx_diff)
                )

        return correl

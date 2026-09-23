    def quantile(
        self,
        q: float | AnyArrayLike | Sequence[float] = 0.5,
        axis: Axis = 0,
        numeric_only: bool = False,
        interpolation: QuantileInterpolation = "linear",
        method: Literal["single", "table"] = "single",
    ) -> Series | DataFrame:
        """
        Return values at the given quantile over requested axis.

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)
            Value between 0 <= q <= 1, the quantile(s) to compute.
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Equals 0 or 'index' for row-wise, 1 or 'columns' for column-wise.
        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

            .. versionchanged:: 2.0.0
                The default value of ``numeric_only`` is now ``False``.

        interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
            This optional parameter specifies the interpolation method to use,
            when the desired quantile lies between two data points `i` and `j`:

            * linear: `i + (j - i) * fraction`, where `fraction` is the
              fractional part of the index surrounded by `i` and `j`.
            * lower: `i`.
            * higher: `j`.
            * nearest: `i` or `j` whichever is nearest.
            * midpoint: (`i` + `j`) / 2.
        method : {'single', 'table'}, default 'single'
            Whether to compute quantiles per-column ('single') or over all columns
            ('table'). When 'table', the only allowed interpolation methods are
            'nearest', 'lower', and 'higher'.

        Returns
        -------
        Series or DataFrame

            If ``q`` is an array, a DataFrame will be returned where the
              index is ``q``, the columns are the columns of self, and the
              values are the quantiles.
            If ``q`` is a float, a Series will be returned where the
              index is the columns of self and the values are the quantiles.

        See Also
        --------
        core.window.rolling.Rolling.quantile: Rolling quantile.
        numpy.percentile: Numpy function to compute the percentile.

        Examples
        --------
        >>> df = pd.DataFrame(np.array([[1, 1], [2, 10], [3, 100], [4, 100]]),
        ...                   columns=['a', 'b'])
        >>> df.quantile(.1)
        a    1.3
        b    3.7
        Name: 0.1, dtype: float64
        >>> df.quantile([.1, .5])
               a     b
        0.1  1.3   3.7
        0.5  2.5  55.0

        Specifying `method='table'` will compute the quantile over all columns.

        >>> df.quantile(.1, method="table", interpolation="nearest")
        a    1
        b    1
        Name: 0.1, dtype: int64
        >>> df.quantile([.1, .5], method="table", interpolation="nearest")
             a    b
        0.1  1    1
        0.5  3  100

        Specifying `numeric_only=False` will also compute the quantile of
        datetime and timedelta data.

        >>> df = pd.DataFrame({'A': [1, 2],
        ...                    'B': [pd.Timestamp('2010'),
        ...                          pd.Timestamp('2011')],
        ...                    'C': [pd.Timedelta('1 days'),
        ...                          pd.Timedelta('2 days')]})
        >>> df.quantile(0.5, numeric_only=False)
        A                    1.5
        B    2010-07-02 12:00:00
        C        1 days 12:00:00
        Name: 0.5, dtype: object
        """
        validate_percentile(q)
        axis = self._get_axis_number(axis)

        if not is_list_like(q):
            # BlockManager.quantile expects listlike, so we wrap and unwrap here
            # error: List item 0 has incompatible type "Union[float, Union[Union[
            # ExtensionArray, ndarray[Any, Any]], Index, Series], Sequence[float]]";
            # expected "float"
            res_df = self.quantile(  # type: ignore[call-overload]
                [q],
                axis=axis,
                numeric_only=numeric_only,
                interpolation=interpolation,
                method=method,
            )
            if method == "single":
                res = res_df.iloc[0]
            else:
                # cannot directly iloc over sparse arrays
                res = res_df.T.iloc[:, 0]
            if axis == 1 and len(self) == 0:
                # GH#41544 try to get an appropriate dtype
                dtype = find_common_type(list(self.dtypes))
                if needs_i8_conversion(dtype):
                    return res.astype(dtype)
            return res

        q = Index(q, dtype=np.float64)
        data = self._get_numeric_data() if numeric_only else self

        if axis == 1:
            data = data.T

        if len(data.columns) == 0:
            # GH#23925 _get_numeric_data may have dropped all columns
            cols = Index([], name=self.columns.name)

            dtype = np.float64
            if axis == 1:
                # GH#41544 try to get an appropriate dtype
                cdtype = find_common_type(list(self.dtypes))
                if needs_i8_conversion(cdtype):
                    dtype = cdtype

            res = self._constructor([], index=q, columns=cols, dtype=dtype)
            return res.__finalize__(self, method="quantile")

        valid_method = {"single", "table"}
        if method not in valid_method:
            raise ValueError(
                f"Invalid method: {method}. Method must be in {valid_method}."
            )
        if method == "single":
            res = data._mgr.quantile(qs=q, interpolation=interpolation)
        elif method == "table":
            valid_interpolation = {"nearest", "lower", "higher"}
            if interpolation not in valid_interpolation:
                raise ValueError(
                    f"Invalid interpolation: {interpolation}. "
                    f"Interpolation must be in {valid_interpolation}"
                )
            # handle degenerate case
            if len(data) == 0:
                if data.ndim == 2:
                    dtype = find_common_type(list(self.dtypes))
                else:
                    dtype = self.dtype
                return self._constructor([], index=q, columns=data.columns, dtype=dtype)

            q_idx = np.quantile(np.arange(len(data)), q, method=interpolation)

            by = data.columns
            if len(by) > 1:
                keys = [data._get_label_or_level_values(x) for x in by]
                indexer = lexsort_indexer(keys)
            else:
                k = data._get_label_or_level_values(by[0])
                indexer = nargsort(k)

            res = data._mgr.take(indexer[q_idx], verify=False)
            res.axes[1] = q

        result = self._constructor_from_mgr(res, axes=res.axes)
        return result.__finalize__(self, method="quantile")

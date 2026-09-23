    def quantile(self, q=0.5, axis=0, numeric_only=True):
        """
        Return values at the given quantile over requested axis, a la
        numpy.percentile.

        Parameters
        ----------
        q : float or array-like, default 0.5 (50% quantile)
            0 <= q <= 1, the quantile(s) to compute
        axis : {0, 1}
            0 for row-wise, 1 for column-wise

        Returns
        -------
        quantiles : Series or DataFrame
            If ``q`` is an array, a DataFrame will be returned where the
            index is ``q``, the columns are the columns of self, and the
            values are the quantiles.
            If ``q`` is a float, a Series will be returned where the
            index is the columns of self and the values are the quantiles.

        Examples
        --------

        >>> df = DataFrame(np.array([[1, 1], [2, 10], [3, 100], [4, 100]]),
                          columns=['a', 'b'])
        >>> df.quantile(.1)
        a    1.3
        b    3.7
        dtype: float64
        >>> df.quantile([.1, .5])
               a     b
        0.1  1.3   3.7
        0.5  2.5  55.0
        """
        per = np.asarray(q) * 100

        if not com.is_list_like(per):
            per = [per]
            q = [q]
            squeeze = True
        else:
            squeeze = False

        def f(arr, per):
            if arr._is_datelike_mixed_type:
                values = _values_from_object(arr).view('i8')
            else:
                values = arr.astype(float)
            values = values[notnull(values)]
            if len(values) == 0:
                return NA
            else:
                return _quantile(values, per)

        data = self._get_numeric_data() if numeric_only else self
        if axis == 1:
            data = data.T

        # need to know which cols are timestamp going in so that we can
        # map timestamp over them after getting the quantile.
        is_dt_col = data.dtypes.map(com.is_datetime64_dtype)
        is_dt_col = is_dt_col[is_dt_col].index

        quantiles = [[f(vals, x) for x in per]
                     for (_, vals) in data.iteritems()]
        result = DataFrame(quantiles, index=data._info_axis, columns=q).T
        if len(is_dt_col) > 0:
            result[is_dt_col] = result[is_dt_col].applymap(lib.Timestamp)
        if squeeze:
            if result.shape == (1, 1):
                result = result.T.iloc[:, 0]  # don't want scalar
            else:
                result = result.T.squeeze()
            result.name = None  # For groupby, so it can set an index name
        return result

    def clip(
        self: NDFrameT,
        lower=None,
        upper=None,
        axis: Axis | None = None,
        inplace: bool_t = False,
        *args,
        **kwargs,
    ) -> NDFrameT | None:
        """
        Trim values at input threshold(s).

        Assigns values outside boundary to boundary values. Thresholds
        can be singular values or array like, and in the latter case
        the clipping is performed element-wise in the specified axis.

        Parameters
        ----------
        lower : float or array-like, default None
            Minimum threshold value. All values below this
            threshold will be set to it. A missing
            threshold (e.g `NA`) will not clip the value.
        upper : float or array-like, default None
            Maximum threshold value. All values above this
            threshold will be set to it. A missing
            threshold (e.g `NA`) will not clip the value.
        axis : {{0 or 'index', 1 or 'columns', None}}, default None
            Align object with lower and upper along the given axis.
            For `Series` this parameter is unused and defaults to `None`.
        inplace : bool, default False
            Whether to perform the operation in place on the data.
        *args, **kwargs
            Additional keywords have no effect but might be accepted
            for compatibility with numpy.

        Returns
        -------
        Series or DataFrame or None
            Same type as calling object with the values outside the
            clip boundaries replaced or None if ``inplace=True``.

        See Also
        --------
        Series.clip : Trim values at input threshold in series.
        DataFrame.clip : Trim values at input threshold in dataframe.
        numpy.clip : Clip (limit) the values in an array.

        Examples
        --------
        >>> data = {'col_0': [9, -3, 0, -1, 5], 'col_1': [-2, -7, 6, 8, -5]}
        >>> df = pd.DataFrame(data)
        >>> df
           col_0  col_1
        0      9     -2
        1     -3     -7
        2      0      6
        3     -1      8
        4      5     -5

        Clips per column using lower and upper thresholds:

        >>> df.clip(-4, 6)
           col_0  col_1
        0      6     -2
        1     -3     -4
        2      0      6
        3     -1      6
        4      5     -4

        Clips using specific lower and upper thresholds per column element:

        >>> t = pd.Series([2, -4, -1, 6, 3])
        >>> t
        0    2
        1   -4
        2   -1
        3    6
        4    3
        dtype: int64

        >>> df.clip(t, t + 4, axis=0)
           col_0  col_1
        0      6      2
        1     -3     -4
        2      0      3
        3      6      8
        4      5      3

        Clips using specific lower threshold per column element, with missing values:

        >>> t = pd.Series([2, -4, np.NaN, 6, 3])
        >>> t
        0    2.0
        1   -4.0
        2    NaN
        3    6.0
        4    3.0
        dtype: float64

        >>> df.clip(t, axis=0)
        col_0  col_1
        0      9      2
        1     -3     -4
        2      0      6
        3      6      8
        4      5      3
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        axis = nv.validate_clip_with_axis(axis, args, kwargs)
        if axis is not None:
            axis = self._get_axis_number(axis)

        # GH 17276
        # numpy doesn't like NaN as a clip value
        # so ignore
        # GH 19992
        # numpy doesn't drop a list-like bound containing NaN
        isna_lower = isna(lower)
        if not is_list_like(lower):
            if np.any(isna_lower):
                lower = None
        elif np.all(isna_lower):
            lower = None
        isna_upper = isna(upper)
        if not is_list_like(upper):
            if np.any(isna_upper):
                upper = None
        elif np.all(isna_upper):
            upper = None

        # GH 2747 (arguments were reversed)
        if (
            lower is not None
            and upper is not None
            and is_scalar(lower)
            and is_scalar(upper)
        ):
            lower, upper = min(lower, upper), max(lower, upper)

        # fast-path for scalars
        if (lower is None or (is_scalar(lower) and is_number(lower))) and (
            upper is None or (is_scalar(upper) and is_number(upper))
        ):
            return self._clip_with_scalar(lower, upper, inplace=inplace)

        result = self
        if lower is not None:
            result = result._clip_with_one_bound(
                lower, method=self.ge, axis=axis, inplace=inplace
            )
        if upper is not None:
            if inplace:
                result = self
            result = result._clip_with_one_bound(
                upper, method=self.le, axis=axis, inplace=inplace
            )

        return result

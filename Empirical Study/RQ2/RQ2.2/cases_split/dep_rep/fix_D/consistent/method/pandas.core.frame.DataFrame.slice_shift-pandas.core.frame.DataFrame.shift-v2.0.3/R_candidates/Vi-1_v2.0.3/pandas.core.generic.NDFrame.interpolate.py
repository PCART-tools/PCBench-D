    def interpolate(
        self: NDFrameT,
        method: str = "linear",
        *,
        axis: Axis = 0,
        limit: int | None = None,
        inplace: bool_t = False,
        limit_direction: str | None = None,
        limit_area: str | None = None,
        downcast: str | None = None,
        **kwargs,
    ) -> NDFrameT | None:
        """
        Fill NaN values using an interpolation method.

        Please note that only ``method='linear'`` is supported for
        DataFrame/Series with a MultiIndex.

        Parameters
        ----------
        method : str, default 'linear'
            Interpolation technique to use. One of:

            * 'linear': Ignore the index and treat the values as equally
              spaced. This is the only method supported on MultiIndexes.
            * 'time': Works on daily and higher resolution data to interpolate
              given length of interval.
            * 'index', 'values': use the actual numerical values of the index.
            * 'pad': Fill in NaNs using existing values.
            * 'nearest', 'zero', 'slinear', 'quadratic', 'cubic',
              'barycentric', 'polynomial': Passed to
              `scipy.interpolate.interp1d`, whereas 'spline' is passed to
              `scipy.interpolate.UnivariateSpline`. These methods use the numerical
              values of the index.  Both 'polynomial' and 'spline' require that
              you also specify an `order` (int), e.g.
              ``df.interpolate(method='polynomial', order=5)``. Note that,
              `slinear` method in Pandas refers to the Scipy first order `spline`
              instead of Pandas first order `spline`.
            * 'krogh', 'piecewise_polynomial', 'spline', 'pchip', 'akima',
              'cubicspline': Wrappers around the SciPy interpolation methods of
              similar names. See `Notes`.
            * 'from_derivatives': Refers to
              `scipy.interpolate.BPoly.from_derivatives` which
              replaces 'piecewise_polynomial' interpolation method in
              scipy 0.18.

        axis : {{0 or 'index', 1 or 'columns', None}}, default None
            Axis to interpolate along. For `Series` this parameter is unused
            and defaults to 0.
        limit : int, optional
            Maximum number of consecutive NaNs to fill. Must be greater than
            0.
        inplace : bool, default False
            Update the data in place if possible.
        limit_direction : {{'forward', 'backward', 'both'}}, Optional
            Consecutive NaNs will be filled in this direction.

            If limit is specified:
                * If 'method' is 'pad' or 'ffill', 'limit_direction' must be 'forward'.
                * If 'method' is 'backfill' or 'bfill', 'limit_direction' must be
                  'backwards'.

            If 'limit' is not specified:
                * If 'method' is 'backfill' or 'bfill', the default is 'backward'
                * else the default is 'forward'

            .. versionchanged:: 1.1.0
                raises ValueError if `limit_direction` is 'forward' or 'both' and
                    method is 'backfill' or 'bfill'.
                raises ValueError if `limit_direction` is 'backward' or 'both' and
                    method is 'pad' or 'ffill'.

        limit_area : {{`None`, 'inside', 'outside'}}, default None
            If limit is specified, consecutive NaNs will be filled with this
            restriction.

            * ``None``: No fill restriction.
            * 'inside': Only fill NaNs surrounded by valid values
              (interpolate).
            * 'outside': Only fill NaNs outside valid values (extrapolate).

        downcast : optional, 'infer' or None, defaults to None
            Downcast dtypes if possible.
        ``**kwargs`` : optional
            Keyword arguments to pass on to the interpolating function.

        Returns
        -------
        Series or DataFrame or None
            Returns the same object type as the caller, interpolated at
            some or all ``NaN`` values or None if ``inplace=True``.

        See Also
        --------
        fillna : Fill missing values using different methods.
        scipy.interpolate.Akima1DInterpolator : Piecewise cubic polynomials
            (Akima interpolator).
        scipy.interpolate.BPoly.from_derivatives : Piecewise polynomial in the
            Bernstein basis.
        scipy.interpolate.interp1d : Interpolate a 1-D function.
        scipy.interpolate.KroghInterpolator : Interpolate polynomial (Krogh
            interpolator).
        scipy.interpolate.PchipInterpolator : PCHIP 1-d monotonic cubic
            interpolation.
        scipy.interpolate.CubicSpline : Cubic spline data interpolator.

        Notes
        -----
        The 'krogh', 'piecewise_polynomial', 'spline', 'pchip' and 'akima'
        methods are wrappers around the respective SciPy implementations of
        similar names. These use the actual numerical values of the index.
        For more information on their behavior, see the
        `SciPy documentation
        <https://docs.scipy.org/doc/scipy/reference/interpolate.html#univariate-interpolation>`__.

        Examples
        --------
        Filling in ``NaN`` in a :class:`~pandas.Series` via linear
        interpolation.

        >>> s = pd.Series([0, 1, np.nan, 3])
        >>> s
        0    0.0
        1    1.0
        2    NaN
        3    3.0
        dtype: float64
        >>> s.interpolate()
        0    0.0
        1    1.0
        2    2.0
        3    3.0
        dtype: float64

        Filling in ``NaN`` in a Series by padding, but filling at most two
        consecutive ``NaN`` at a time.

        >>> s = pd.Series([np.nan, "single_one", np.nan,
        ...                "fill_two_more", np.nan, np.nan, np.nan,
        ...                4.71, np.nan])
        >>> s
        0              NaN
        1       single_one
        2              NaN
        3    fill_two_more
        4              NaN
        5              NaN
        6              NaN
        7             4.71
        8              NaN
        dtype: object
        >>> s.interpolate(method='pad', limit=2)
        0              NaN
        1       single_one
        2       single_one
        3    fill_two_more
        4    fill_two_more
        5    fill_two_more
        6              NaN
        7             4.71
        8             4.71
        dtype: object

        Filling in ``NaN`` in a Series via polynomial interpolation or splines:
        Both 'polynomial' and 'spline' methods require that you also specify
        an ``order`` (int).

        >>> s = pd.Series([0, 2, np.nan, 8])
        >>> s.interpolate(method='polynomial', order=2)
        0    0.000000
        1    2.000000
        2    4.666667
        3    8.000000
        dtype: float64

        Fill the DataFrame forward (that is, going down) along each column
        using linear interpolation.

        Note how the last entry in column 'a' is interpolated differently,
        because there is no entry after it to use for interpolation.
        Note how the first entry in column 'b' remains ``NaN``, because there
        is no entry before it to use for interpolation.

        >>> df = pd.DataFrame([(0.0, np.nan, -1.0, 1.0),
        ...                    (np.nan, 2.0, np.nan, np.nan),
        ...                    (2.0, 3.0, np.nan, 9.0),
        ...                    (np.nan, 4.0, -4.0, 16.0)],
        ...                   columns=list('abcd'))
        >>> df
             a    b    c     d
        0  0.0  NaN -1.0   1.0
        1  NaN  2.0  NaN   NaN
        2  2.0  3.0  NaN   9.0
        3  NaN  4.0 -4.0  16.0
        >>> df.interpolate(method='linear', limit_direction='forward', axis=0)
             a    b    c     d
        0  0.0  NaN -1.0   1.0
        1  1.0  2.0 -2.0   5.0
        2  2.0  3.0 -3.0   9.0
        3  2.0  4.0 -4.0  16.0

        Using polynomial interpolation.

        >>> df['d'].interpolate(method='polynomial', order=2)
        0     1.0
        1     4.0
        2     9.0
        3    16.0
        Name: d, dtype: float64
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        axis = self._get_axis_number(axis)

        fillna_methods = ["ffill", "bfill", "pad", "backfill"]
        should_transpose = axis == 1 and method not in fillna_methods

        obj = self.T if should_transpose else self

        if obj.empty:
            return self.copy()

        if method not in fillna_methods:
            axis = self._info_axis_number

        if isinstance(obj.index, MultiIndex) and method != "linear":
            raise ValueError(
                "Only `method=linear` interpolation is supported on MultiIndexes."
            )

        # Set `limit_direction` depending on `method`
        if limit_direction is None:
            limit_direction = (
                "backward" if method in ("backfill", "bfill") else "forward"
            )
        else:
            if method in ("pad", "ffill") and limit_direction != "forward":
                raise ValueError(
                    f"`limit_direction` must be 'forward' for method `{method}`"
                )
            if method in ("backfill", "bfill") and limit_direction != "backward":
                raise ValueError(
                    f"`limit_direction` must be 'backward' for method `{method}`"
                )

        if obj.ndim == 2 and np.all(obj.dtypes == np.dtype("object")):
            raise TypeError(
                "Cannot interpolate with all object-dtype columns "
                "in the DataFrame. Try setting at least one "
                "column to a numeric dtype."
            )

        # create/use the index
        if method == "linear":
            # prior default
            index = Index(np.arange(len(obj.index)))
        else:
            index = obj.index
            methods = {"index", "values", "nearest", "time"}
            is_numeric_or_datetime = (
                is_numeric_dtype(index.dtype)
                or is_datetime64_any_dtype(index.dtype)
                or is_timedelta64_dtype(index.dtype)
            )
            if method not in methods and not is_numeric_or_datetime:
                raise ValueError(
                    "Index column must be numeric or datetime type when "
                    f"using {method} method other than linear. "
                    "Try setting a numeric or datetime index column before "
                    "interpolating."
                )

        if isna(index).any():
            raise NotImplementedError(
                "Interpolation with NaNs in the index "
                "has not been implemented. Try filling "
                "those NaNs before interpolating."
            )
        new_data = obj._mgr.interpolate(
            method=method,
            axis=axis,
            index=index,
            limit=limit,
            limit_direction=limit_direction,
            limit_area=limit_area,
            inplace=inplace,
            downcast=downcast,
            **kwargs,
        )

        result = self._constructor(new_data)
        if should_transpose:
            result = result.T
        if inplace:
            return self._update_inplace(result)
        else:
            return result.__finalize__(self, method="interpolate")

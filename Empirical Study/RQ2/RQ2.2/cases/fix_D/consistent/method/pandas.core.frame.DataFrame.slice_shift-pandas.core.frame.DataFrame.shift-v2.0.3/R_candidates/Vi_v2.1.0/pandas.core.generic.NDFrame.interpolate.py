    @final
    def interpolate(
        self,
        method: InterpolateOptions = "linear",
        *,
        axis: Axis = 0,
        limit: int | None = None,
        inplace: bool_t = False,
        limit_direction: Literal["forward", "backward", "both"] | None = None,
        limit_area: Literal["inside", "outside"] | None = None,
        downcast: Literal["infer"] | None | lib.NoDefault = lib.no_default,
        **kwargs,
    ) -> Self | None:
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
              `scipy.interpolate.BPoly.from_derivatives`.

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

            .. deprecated:: 2.1.0

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
        if downcast is not lib.no_default:
            # GH#40988
            warnings.warn(
                f"The 'downcast' keyword in {type(self).__name__}.interpolate "
                "is deprecated and will be removed in a future version. "
                "Call result.infer_objects(copy=False) on the result instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            downcast = None
        if downcast is not None and downcast != "infer":
            raise ValueError("downcast must be either None or 'infer'")

        inplace = validate_bool_kwarg(inplace, "inplace")

        if inplace:
            if not PYPY and using_copy_on_write():
                if sys.getrefcount(self) <= REF_COUNT:
                    warnings.warn(
                        _chained_assignment_method_msg,
                        ChainedAssignmentError,
                        stacklevel=2,
                    )

        axis = self._get_axis_number(axis)

        if self.empty:
            if inplace:
                return None
            return self.copy()

        if not isinstance(method, str):
            raise ValueError("'method' should be a string, not None.")

        fillna_methods = ["ffill", "bfill", "pad", "backfill"]
        if method.lower() in fillna_methods:
            # GH#53581
            warnings.warn(
                f"{type(self).__name__}.interpolate with method={method} is "
                "deprecated and will raise in a future version. "
                "Use obj.ffill() or obj.bfill() instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            obj, should_transpose = self, False
        else:
            obj, should_transpose = (self.T, True) if axis == 1 else (self, False)
            if np.any(obj.dtypes == object):
                # GH#53631
                if not (obj.ndim == 2 and np.all(obj.dtypes == object)):
                    # don't warn in cases that already raise
                    warnings.warn(
                        f"{type(self).__name__}.interpolate with object dtype is "
                        "deprecated and will raise in a future version. Call "
                        "obj.infer_objects(copy=False) before interpolating instead.",
                        FutureWarning,
                        stacklevel=find_stack_level(),
                    )

        if "fill_value" in kwargs:
            raise ValueError(
                "'fill_value' is not a valid keyword for "
                f"{type(self).__name__}.interpolate"
            )

        if isinstance(obj.index, MultiIndex) and method != "linear":
            raise ValueError(
                "Only `method=linear` interpolation is supported on MultiIndexes."
            )

        limit_direction = missing.infer_limit_direction(limit_direction, method)

        if obj.ndim == 2 and np.all(obj.dtypes == object):
            raise TypeError(
                "Cannot interpolate with all object-dtype columns "
                "in the DataFrame. Try setting at least one "
                "column to a numeric dtype."
            )

        if method.lower() in fillna_methods:
            # TODO(3.0): remove this case
            # TODO: warn/raise on limit_direction or kwargs which are ignored?
            #  as of 2023-06-26 no tests get here with either
            if not self._mgr.is_single_block and axis == 1:
                # GH#53898
                if inplace:
                    raise NotImplementedError()
                obj, axis, should_transpose = self.T, 1 - axis, True

            new_data = obj._mgr.pad_or_backfill(
                method=method,
                axis=self._get_block_manager_axis(axis),
                limit=limit,
                limit_area=limit_area,
                inplace=inplace,
                downcast=downcast,
            )
        else:
            index = missing.get_interp_index(method, obj.index)
            new_data = obj._mgr.interpolate(
                method=method,
                index=index,
                limit=limit,
                limit_direction=limit_direction,
                limit_area=limit_area,
                inplace=inplace,
                downcast=downcast,
                **kwargs,
            )

        result = self._constructor_from_mgr(new_data, axes=new_data.axes)
        if should_transpose:
            result = result.T
        if inplace:
            return self._update_inplace(result)
        else:
            return result.__finalize__(self, method="interpolate")

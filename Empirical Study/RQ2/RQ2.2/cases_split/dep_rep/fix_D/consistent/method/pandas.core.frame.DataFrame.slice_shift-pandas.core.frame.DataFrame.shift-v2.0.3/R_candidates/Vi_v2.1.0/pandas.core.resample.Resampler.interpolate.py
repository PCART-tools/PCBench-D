    def interpolate(
        self,
        method: InterpolateOptions = "linear",
        *,
        axis: Axis = 0,
        limit: int | None = None,
        inplace: bool = False,
        limit_direction: Literal["forward", "backward", "both"] = "forward",
        limit_area=None,
        downcast=lib.no_default,
        **kwargs,
    ):
        """
        Interpolate values between target timestamps according to different methods.

        The original index is first reindexed to target timestamps
        (see :meth:`core.resample.Resampler.asfreq`),
        then the interpolation of ``NaN`` values via :meth`DataFrame.interpolate`
        happens.

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

            .. deprecated::2.1.0

        ``**kwargs`` : optional
            Keyword arguments to pass on to the interpolating function.

        Returns
        -------
        DataFrame or Series
            Interpolated values at the specified freq.

        See Also
        --------
        core.resample.Resampler.asfreq: Return the values at the new freq,
            essentially a reindex.
        DataFrame.interpolate: Fill NaN values using an interpolation method.

        Notes
        -----
        For high-frequent or non-equidistant time-series with timestamps
        the reindexing followed by interpolation may lead to information loss
        as shown in the last example.

        Examples
        --------

        >>> import datetime as dt
        >>> timesteps = [
        ...    dt.datetime(2023, 3, 1, 7, 0, 0),
        ...    dt.datetime(2023, 3, 1, 7, 0, 1),
        ...    dt.datetime(2023, 3, 1, 7, 0, 2),
        ...    dt.datetime(2023, 3, 1, 7, 0, 3),
        ...    dt.datetime(2023, 3, 1, 7, 0, 4)]
        >>> series = pd.Series(data=[1, -1, 2, 1, 3], index=timesteps)
        >>> series
        2023-03-01 07:00:00    1
        2023-03-01 07:00:01   -1
        2023-03-01 07:00:02    2
        2023-03-01 07:00:03    1
        2023-03-01 07:00:04    3
        dtype: int64

        Upsample the dataframe to 0.5Hz by providing the period time of 2s.

        >>> series.resample("2s").interpolate("linear")
        2023-03-01 07:00:00    1
        2023-03-01 07:00:02    2
        2023-03-01 07:00:04    3
        Freq: 2S, dtype: int64

        Downsample the dataframe to 2Hz by providing the period time of 500ms.

        >>> series.resample("500ms").interpolate("linear")
        2023-03-01 07:00:00.000    1.0
        2023-03-01 07:00:00.500    0.0
        2023-03-01 07:00:01.000   -1.0
        2023-03-01 07:00:01.500    0.5
        2023-03-01 07:00:02.000    2.0
        2023-03-01 07:00:02.500    1.5
        2023-03-01 07:00:03.000    1.0
        2023-03-01 07:00:03.500    2.0
        2023-03-01 07:00:04.000    3.0
        Freq: 500L, dtype: float64

        Internal reindexing with ``as_freq()`` prior to interpolation leads to
        an interpolated timeseries on the basis the reindexed timestamps (anchors).
        Since not all datapoints from original series become anchors,
        it can lead to misleading interpolation results as in the following example:

        >>> series.resample("400ms").interpolate("linear")
        2023-03-01 07:00:00.000    1.0
        2023-03-01 07:00:00.400    1.2
        2023-03-01 07:00:00.800    1.4
        2023-03-01 07:00:01.200    1.6
        2023-03-01 07:00:01.600    1.8
        2023-03-01 07:00:02.000    2.0
        2023-03-01 07:00:02.400    2.2
        2023-03-01 07:00:02.800    2.4
        2023-03-01 07:00:03.200    2.6
        2023-03-01 07:00:03.600    2.8
        2023-03-01 07:00:04.000    3.0
        Freq: 400L, dtype: float64

        Note that the series erroneously increases between two anchors
        ``07:00:00`` and ``07:00:02``.
        """
        assert downcast is lib.no_default  # just checking coverage
        result = self._upsample("asfreq")
        return result.interpolate(
            method=method,
            axis=axis,
            limit=limit,
            inplace=inplace,
            limit_direction=limit_direction,
            limit_area=limit_area,
            downcast=downcast,
            **kwargs,
        )

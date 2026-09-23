    @classmethod
    def _add_numeric_operations(cls):
        """ add the operations to the cls; evaluate the doc strings again """

        axis_descr = "{%s}" % ', '.join([
            "{0} ({1})".format(a, i) for i, a in enumerate(cls._AXIS_ORDERS)
        ])
        name = (cls._constructor_sliced.__name__
                if cls._AXIS_LEN > 1 else 'scalar')
        _num_doc = """

%(desc)s

Parameters
----------
axis : """ + axis_descr + """
skipna : boolean, default True
    Exclude NA/null values. If an entire row/column is NA, the result
    will be NA
level : int, default None
        If the axis is a MultiIndex (hierarchical), count along a
        particular level, collapsing into a """ + name + """
numeric_only : boolean, default None
    Include only float, int, boolean data. If None, will attempt to use
    everything, then use only numeric data

Returns
-------
%(outname)s : """ + name + " or " + cls.__name__ + " (if level specified)\n"

        _cnum_doc = """

Parameters
----------
axis : """ + axis_descr + """
skipna : boolean, default True
    Exclude NA/null values. If an entire row/column is NA, the result
    will be NA

Returns
-------
%(outname)s : """ + name + "\n"

        def _make_stat_function(name, desc, f):

            @Substitution(outname=name, desc=desc)
            @Appender(_num_doc)
            def stat_func(self, axis=None, skipna=None, level=None,
                          numeric_only=None, **kwargs):
                if skipna is None:
                    skipna = True
                if axis is None:
                    axis = self._stat_axis_number
                if level is not None:
                    return self._agg_by_level(name, axis=axis, level=level,
                                              skipna=skipna)
                return self._reduce(f, axis=axis,
                                    skipna=skipna, numeric_only=numeric_only)
            stat_func.__name__ = name
            return stat_func

        cls.sum = _make_stat_function(
            'sum', 'Return the sum of the values for the requested axis',
            nanops.nansum)
        cls.mean = _make_stat_function(
            'mean', 'Return the mean of the values for the requested axis',
            nanops.nanmean)
        cls.skew = _make_stat_function(
            'skew',
            'Return unbiased skew over requested axis\nNormalized by N-1',
            nanops.nanskew)
        cls.kurt = _make_stat_function(
            'kurt',
            'Return unbiased kurtosis over requested axis\nNormalized by N-1',
            nanops.nankurt)
        cls.kurtosis = cls.kurt
        cls.prod = _make_stat_function(
            'prod', 'Return the product of the values for the requested axis',
            nanops.nanprod)
        cls.product = cls.prod
        cls.median = _make_stat_function(
            'median', 'Return the median of the values for the requested axis',
            nanops.nanmedian)
        cls.max = _make_stat_function('max', """
This method returns the maximum of the values in the object. If you
want the *index* of the maximum, use ``idxmax``. This is the
equivalent of the ``numpy.ndarray`` method ``argmax``.""", nanops.nanmax)
        cls.min = _make_stat_function('min', """
This method returns the minimum of the values in the object. If you
want the *index* of the minimum, use ``idxmin``. This is the
equivalent of the ``numpy.ndarray`` method ``argmin``.""", nanops.nanmin)

        @Substitution(outname='mad',
                      desc="Return the mean absolute deviation of the values "
                           "for the requested axis")
        @Appender(_num_doc)
        def mad(self,  axis=None, skipna=None, level=None, **kwargs):
            if skipna is None:
                skipna = True
            if axis is None:
                axis = self._stat_axis_number
            if level is not None:
                return self._agg_by_level('mad', axis=axis, level=level,
                                          skipna=skipna)

            data = self._get_numeric_data()
            if axis == 0:
                demeaned = data - data.mean(axis=0)
            else:
                demeaned = data.sub(data.mean(axis=1), axis=0)
            return np.abs(demeaned).mean(axis=axis, skipna=skipna)
        cls.mad = mad

        @Substitution(outname='variance',
                      desc="Return unbiased variance over requested "
                           "axis\nNormalized by N-1")
        @Appender(_num_doc)
        def var(self, axis=None, skipna=None, level=None, ddof=1, **kwargs):
            if skipna is None:
                skipna = True
            if axis is None:
                axis = self._stat_axis_number
            if level is not None:
                return self._agg_by_level('var', axis=axis, level=level,
                                          skipna=skipna, ddof=ddof)

            return self._reduce(nanops.nanvar, axis=axis, skipna=skipna,
                                ddof=ddof)
        cls.var = var

        @Substitution(outname='stdev',
                      desc="Return unbiased standard deviation over requested "
                           "axis\nNormalized by N-1")
        @Appender(_num_doc)
        def std(self, axis=None, skipna=None, level=None, ddof=1, **kwargs):
            if skipna is None:
                skipna = True
            if axis is None:
                axis = self._stat_axis_number
            if level is not None:
                return self._agg_by_level('std', axis=axis, level=level,
                                          skipna=skipna, ddof=ddof)
            result = self.var(axis=axis, skipna=skipna, ddof=ddof)
            if getattr(result, 'ndim', 0) > 0:
                return result.apply(np.sqrt)
            return np.sqrt(result)
        cls.std = std

        @Substitution(outname='compounded',
                      desc="Return the compound percentage of the values for "
                           "the requested axis")
        @Appender(_num_doc)
        def compound(self, axis=None, skipna=None, level=None, **kwargs):
            if skipna is None:
                skipna = True
            return (1 + self).prod(axis=axis, skipna=skipna, level=level) - 1
        cls.compound = compound

        def _make_cum_function(name, accum_func, mask_a, mask_b):

            @Substitution(outname=name)
            @Appender("Return cumulative {0} over requested axis.".format(name)
                      + _cnum_doc)
            def func(self, axis=None, dtype=None, out=None, skipna=True,
                     **kwargs):
                if axis is None:
                    axis = self._stat_axis_number
                else:
                    axis = self._get_axis_number(axis)

                y = _values_from_object(self).copy()
                if not issubclass(y.dtype.type, (np.integer, np.bool_)):
                    mask = isnull(self)
                    if skipna:
                        np.putmask(y, mask, mask_a)
                    result = accum_func(y, axis)
                    if skipna:
                        np.putmask(result, mask, mask_b)
                else:
                    result = accum_func(y, axis)

                d = self._construct_axes_dict()
                d['copy'] = False
                return self._constructor(result, **d).__finalize__(self)

            func.__name__ = name
            return func

        cls.cummin = _make_cum_function(
            'min', lambda y, axis: np.minimum.accumulate(y, axis),
            np.inf, np.nan)
        cls.cumsum = _make_cum_function(
            'sum', lambda y, axis: y.cumsum(axis), 0., np.nan)
        cls.cumprod = _make_cum_function(
            'prod', lambda y, axis: y.cumprod(axis), 1., np.nan)
        cls.cummax = _make_cum_function(
            'max', lambda y, axis: np.maximum.accumulate(y, axis),
            -np.inf, np.nan)

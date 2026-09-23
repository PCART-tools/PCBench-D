    @classmethod
    def _add_numeric_operations(cls):
        """Add the operations to the cls; evaluate the doc strings again"""

        axis_descr, name, name2 = _doc_parms(cls)

        cls.any = _make_logical_function(
            cls, 'any', name, name2, axis_descr,
            _any_desc, nanops.nanany, _any_examples, _any_see_also)
        cls.all = _make_logical_function(
            cls, 'all', name, name2, axis_descr, _all_doc,
            nanops.nanall, _all_examples, _all_see_also)

        @Substitution(outname='mad',
                      desc="Return the mean absolute deviation of the values "
                           "for the requested axis",
                      name1=name, name2=name2, axis_descr=axis_descr,
                      min_count='', examples='')
        @Appender(_num_doc)
        def mad(self, axis=None, skipna=None, level=None):
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

        cls.sem = _make_stat_function_ddof(
            cls, 'sem', name, name2, axis_descr,
            "Return unbiased standard error of the mean over requested "
            "axis.\n\nNormalized by N-1 by default. This can be changed "
            "using the ddof argument",
            nanops.nansem)
        cls.var = _make_stat_function_ddof(
            cls, 'var', name, name2, axis_descr,
            "Return unbiased variance over requested axis.\n\nNormalized by "
            "N-1 by default. This can be changed using the ddof argument",
            nanops.nanvar)
        cls.std = _make_stat_function_ddof(
            cls, 'std', name, name2, axis_descr,
            "Return sample standard deviation over requested axis."
            "\n\nNormalized by N-1 by default. This can be changed using the "
            "ddof argument",
            nanops.nanstd)

        @Substitution(outname='compounded',
                      desc="Return the compound percentage of the values for "
                      "the requested axis", name1=name, name2=name2,
                      axis_descr=axis_descr,
                      min_count='', examples='')
        @Appender(_num_doc)
        def compound(self, axis=None, skipna=None, level=None):
            if skipna is None:
                skipna = True
            return (1 + self).prod(axis=axis, skipna=skipna, level=level) - 1

        cls.compound = compound

        cls.cummin = _make_cum_function(
            cls, 'cummin', name, name2, axis_descr, "minimum",
            lambda y, axis: np.minimum.accumulate(y, axis), "min",
            np.inf, np.nan, _cummin_examples)
        cls.cumsum = _make_cum_function(
            cls, 'cumsum', name, name2, axis_descr, "sum",
            lambda y, axis: y.cumsum(axis), "sum", 0.,
            np.nan, _cumsum_examples)
        cls.cumprod = _make_cum_function(
            cls, 'cumprod', name, name2, axis_descr, "product",
            lambda y, axis: y.cumprod(axis), "prod", 1.,
            np.nan, _cumprod_examples)
        cls.cummax = _make_cum_function(
            cls, 'cummax', name, name2, axis_descr, "maximum",
            lambda y, axis: np.maximum.accumulate(y, axis), "max",
            -np.inf, np.nan, _cummax_examples)

        cls.sum = _make_min_count_stat_function(
            cls, 'sum', name, name2, axis_descr,
            'Return the sum of the values for the requested axis',
            nanops.nansum, _sum_examples)
        cls.mean = _make_stat_function(
            cls, 'mean', name, name2, axis_descr,
            'Return the mean of the values for the requested axis',
            nanops.nanmean)
        cls.skew = _make_stat_function(
            cls, 'skew', name, name2, axis_descr,
            'Return unbiased skew over requested axis\nNormalized by N-1',
            nanops.nanskew)
        cls.kurt = _make_stat_function(
            cls, 'kurt', name, name2, axis_descr,
            "Return unbiased kurtosis over requested axis using Fisher's "
            "definition of\nkurtosis (kurtosis of normal == 0.0). Normalized "
            "by N-1\n",
            nanops.nankurt)
        cls.kurtosis = cls.kurt
        cls.prod = _make_min_count_stat_function(
            cls, 'prod', name, name2, axis_descr,
            'Return the product of the values for the requested axis',
            nanops.nanprod, _prod_examples)
        cls.product = cls.prod
        cls.median = _make_stat_function(
            cls, 'median', name, name2, axis_descr,
            'Return the median of the values for the requested axis',
            nanops.nanmedian)
        cls.max = _make_stat_function(
            cls, 'max', name, name2, axis_descr,
            """This method returns the maximum of the values in the object.
            If you want the *index* of the maximum, use ``idxmax``. This is
            the equivalent of the ``numpy.ndarray`` method ``argmax``.""",
            nanops.nanmax)
        cls.min = _make_stat_function(
            cls, 'min', name, name2, axis_descr,
            """This method returns the minimum of the values in the object.
            If you want the *index* of the minimum, use ``idxmin``. This is
            the equivalent of the ``numpy.ndarray`` method ``argmin``.""",
            nanops.nanmin)

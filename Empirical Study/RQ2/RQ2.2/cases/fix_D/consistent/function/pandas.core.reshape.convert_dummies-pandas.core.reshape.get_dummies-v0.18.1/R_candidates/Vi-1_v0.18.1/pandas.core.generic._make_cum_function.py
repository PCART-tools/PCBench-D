def _make_cum_function(cls, name, name1, name2, axis_descr, desc, accum_func,
                       mask_a, mask_b):
    @Substitution(outname=name, desc=desc, name1=name1, name2=name2,
                  axis_descr=axis_descr)
    @Appender("Return cumulative {0} over requested axis.".format(name) +
              _cnum_doc)
    def cum_func(self, axis=None, dtype=None, out=None, skipna=True, **kwargs):
        nv.validate_cum_func(tuple(), kwargs)
        if axis is None:
            axis = self._stat_axis_number
        else:
            axis = self._get_axis_number(axis)

        y = _values_from_object(self).copy()

        if (skipna and
                issubclass(y.dtype.type, (np.datetime64, np.timedelta64))):
            result = accum_func(y, axis)
            mask = isnull(self)
            np.putmask(result, mask, pd.tslib.iNaT)
        elif skipna and not issubclass(y.dtype.type, (np.integer, np.bool_)):
            mask = isnull(self)
            np.putmask(y, mask, mask_a)
            result = accum_func(y, axis)
            np.putmask(result, mask, mask_b)
        else:
            result = accum_func(y, axis)

        d = self._construct_axes_dict()
        d['copy'] = False
        return self._constructor(result, **d).__finalize__(self)

    return set_function_name(cum_func, name, cls)

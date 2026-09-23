def _make_stat_function(cls, name, name1, name2, axis_descr, desc, f):
    @Substitution(outname=name, desc=desc, name1=name1, name2=name2,
                  axis_descr=axis_descr)
    @Appender(_num_doc)
    def stat_func(self, axis=None, skipna=None, level=None, numeric_only=None,
                  **kwargs):
        nv.validate_stat_func(tuple(), kwargs)
        if skipna is None:
            skipna = True
        if axis is None:
            axis = self._stat_axis_number
        if level is not None:
            return self._agg_by_level(name, axis=axis, level=level,
                                      skipna=skipna)
        return self._reduce(f, name, axis=axis, skipna=skipna,
                            numeric_only=numeric_only)

    return set_function_name(stat_func, name, cls)

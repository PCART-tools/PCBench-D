def _make_logical_function(cls, name, name1, name2, axis_descr, desc, f):
    @Substitution(outname=name, desc=desc, name1=name1, name2=name2,
                  axis_descr=axis_descr)
    @Appender(_bool_doc)
    def logical_func(self, axis=None, bool_only=None, skipna=None, level=None,
                     **kwargs):
        nv.validate_logical_func(tuple(), kwargs)
        if skipna is None:
            skipna = True
        if axis is None:
            axis = self._stat_axis_number
        if level is not None:
            if bool_only is not None:
                raise NotImplementedError("Option bool_only is not "
                                          "implemented with option level.")
            return self._agg_by_level(name, axis=axis, level=level,
                                      skipna=skipna)
        return self._reduce(f, axis=axis, skipna=skipna,
                            numeric_only=bool_only, filter_type='bool',
                            name=name)

    return set_function_name(logical_func, name, cls)

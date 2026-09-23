    def sem(self, axis=None, dtype=None, out=None, ddof=1, keepdims=False,
            skipna=True):
        nv.validate_stat_ddof_func((), dict(dtype=dtype, out=out,
                                            keepdims=keepdims),
                                   fname='sem')
        return nanops.nansem(self._ndarray, axis=axis, skipna=skipna,
                             ddof=ddof)

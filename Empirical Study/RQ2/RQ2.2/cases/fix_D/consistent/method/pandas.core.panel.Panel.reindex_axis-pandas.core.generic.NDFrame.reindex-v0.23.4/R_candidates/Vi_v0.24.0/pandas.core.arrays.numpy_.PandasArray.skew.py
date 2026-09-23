    def skew(self, axis=None, dtype=None, out=None, keepdims=False,
             skipna=True):
        nv.validate_stat_ddof_func((), dict(dtype=dtype, out=out,
                                            keepdims=keepdims),
                                   fname='skew')
        return nanops.nanskew(self._ndarray, axis=axis, skipna=skipna)

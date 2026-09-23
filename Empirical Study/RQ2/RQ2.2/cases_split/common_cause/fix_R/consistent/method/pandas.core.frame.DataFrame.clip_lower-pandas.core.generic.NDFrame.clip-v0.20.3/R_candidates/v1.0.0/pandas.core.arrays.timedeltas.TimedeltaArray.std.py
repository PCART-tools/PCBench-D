    def std(
        self,
        axis=None,
        dtype=None,
        out=None,
        ddof: int = 1,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        nv.validate_stat_ddof_func(
            (), dict(dtype=dtype, out=out, keepdims=keepdims), fname="std"
        )
        if not len(self):
            return NaT
        if not skipna and self._hasnans:
            return NaT

        result = nanops.nanstd(self._data, axis=axis, skipna=skipna, ddof=ddof)
        return Timedelta(result)

    def sum(
        self,
        axis=None,
        dtype=None,
        out=None,
        keepdims: bool = False,
        initial=None,
        skipna: bool = True,
        min_count: int = 0,
    ):
        nv.validate_sum(
            (), dict(dtype=dtype, out=out, keepdims=keepdims, initial=initial)
        )
        if not len(self):
            return NaT
        if not skipna and self._hasnans:
            return NaT

        result = nanops.nansum(
            self._data, axis=axis, skipna=skipna, min_count=min_count
        )
        return Timedelta(result)

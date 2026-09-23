    @final
    def _accum_func(
        self,
        name: str,
        func,
        axis: Axis | None = None,
        skipna: bool_t = True,
        *args,
        **kwargs,
    ):
        skipna = nv.validate_cum_func_with_skipna(skipna, args, kwargs, name)
        if axis is None:
            axis = self._stat_axis_number
        else:
            axis = self._get_axis_number(axis)

        if axis == 1:
            return self.T._accum_func(
                name, func, axis=0, skipna=skipna, *args, **kwargs
            ).T

        def block_accum_func(blk_values):
            values = blk_values.T if hasattr(blk_values, "T") else blk_values

            result = nanops.na_accum_func(values, func, skipna=skipna)

            result = result.T if hasattr(result, "T") else result
            return result

        result = self._mgr.apply(block_accum_func)

        return self._constructor(result).__finalize__(self, method=name)

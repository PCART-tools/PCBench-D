    def cumsum(self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs):
        return self._accum_func("cumsum", np.cumsum, axis, skipna, *args, **kwargs)

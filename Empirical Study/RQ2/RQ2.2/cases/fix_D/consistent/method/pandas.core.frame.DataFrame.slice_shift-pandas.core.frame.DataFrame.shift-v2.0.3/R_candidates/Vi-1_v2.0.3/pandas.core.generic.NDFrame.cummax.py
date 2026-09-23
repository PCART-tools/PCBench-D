    def cummax(self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs):
        return self._accum_func(
            "cummax", np.maximum.accumulate, axis, skipna, *args, **kwargs
        )

    def cummin(self, axis: Axis | None = None, skipna: bool_t = True, *args, **kwargs):
        return self._accum_func(
            "cummin", np.minimum.accumulate, axis, skipna, *args, **kwargs
        )

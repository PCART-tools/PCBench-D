    def min(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "min", args, kwargs)
        nv.validate_resampler_func("min", args, kwargs)
        return self._downsample("min", numeric_only=numeric_only, min_count=min_count)

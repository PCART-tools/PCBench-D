    def max(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "max", args, kwargs)
        nv.validate_resampler_func("max", args, kwargs)
        return self._downsample("max", numeric_only=numeric_only, min_count=min_count)

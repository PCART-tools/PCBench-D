    def sum(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "sum", args, kwargs)
        nv.validate_resampler_func("sum", args, kwargs)
        return self._downsample("sum", numeric_only=numeric_only, min_count=min_count)

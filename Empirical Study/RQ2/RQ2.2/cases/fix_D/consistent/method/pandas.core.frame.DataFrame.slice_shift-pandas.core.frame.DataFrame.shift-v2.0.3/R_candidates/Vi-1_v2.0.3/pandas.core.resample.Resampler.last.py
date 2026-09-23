    @doc(GroupBy.last)
    def last(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "last", args, kwargs)
        nv.validate_resampler_func("last", args, kwargs)
        return self._downsample("last", numeric_only=numeric_only, min_count=min_count)

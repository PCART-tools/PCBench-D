    @doc(GroupBy.first)
    def first(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "first", args, kwargs)
        nv.validate_resampler_func("first", args, kwargs)
        return self._downsample("first", numeric_only=numeric_only, min_count=min_count)

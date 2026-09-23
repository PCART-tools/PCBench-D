    @doc(GroupBy.prod)
    def prod(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "prod", args, kwargs)
        nv.validate_resampler_func("prod", args, kwargs)
        return self._downsample("prod", numeric_only=numeric_only, min_count=min_count)

    @doc(GroupBy.sem)
    def sem(
        self,
        ddof: int = 1,
        numeric_only: bool = False,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "sem", args, kwargs)
        nv.validate_resampler_func("sem", args, kwargs)
        return self._downsample("sem", ddof=ddof, numeric_only=numeric_only)

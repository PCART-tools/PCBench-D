    @doc(GroupBy.median)
    def median(self, numeric_only: bool = False, *args, **kwargs):
        maybe_warn_args_and_kwargs(type(self), "median", args, kwargs)
        nv.validate_resampler_func("median", args, kwargs)
        return self._downsample("median", numeric_only=numeric_only)

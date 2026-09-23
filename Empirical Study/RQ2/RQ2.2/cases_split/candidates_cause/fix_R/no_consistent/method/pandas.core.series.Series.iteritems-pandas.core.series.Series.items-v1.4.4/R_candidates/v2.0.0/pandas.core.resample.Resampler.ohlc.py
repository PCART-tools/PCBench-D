    @doc(GroupBy.ohlc)
    def ohlc(
        self,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "ohlc", args, kwargs)
        nv.validate_resampler_func("ohlc", args, kwargs)
        return self._downsample("ohlc")

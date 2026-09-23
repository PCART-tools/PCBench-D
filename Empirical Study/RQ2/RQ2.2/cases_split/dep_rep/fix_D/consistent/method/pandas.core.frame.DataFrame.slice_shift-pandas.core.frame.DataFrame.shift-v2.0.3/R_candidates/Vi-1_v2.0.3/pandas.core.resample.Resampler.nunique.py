    @doc(SeriesGroupBy.nunique)
    def nunique(
        self,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "nunique", args, kwargs)
        nv.validate_resampler_func("nunique", args, kwargs)
        return self._downsample("nunique")

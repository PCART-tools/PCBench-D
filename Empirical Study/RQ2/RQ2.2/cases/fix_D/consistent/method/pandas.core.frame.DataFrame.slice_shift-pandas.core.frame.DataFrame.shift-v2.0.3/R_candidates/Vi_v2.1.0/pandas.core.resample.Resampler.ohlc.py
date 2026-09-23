    @doc(GroupBy.ohlc)
    def ohlc(
        self,
        *args,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "ohlc", args, kwargs)
        nv.validate_resampler_func("ohlc", args, kwargs)

        ax = self.ax
        obj = self._obj_with_exclusions
        if len(ax) == 0:
            # GH#42902
            obj = obj.copy()
            obj.index = _asfreq_compat(obj.index, self.freq)
            if obj.ndim == 1:
                obj = obj.to_frame()
                obj = obj.reindex(["open", "high", "low", "close"], axis=1)
            else:
                mi = MultiIndex.from_product(
                    [obj.columns, ["open", "high", "low", "close"]]
                )
                obj = obj.reindex(mi, axis=1)
            return obj

        return self._downsample("ohlc")

    @doc(Index.astype)
    def astype(self, dtype, copy: bool = True, how=lib.no_default):
        dtype = pandas_dtype(dtype)

        if how is not lib.no_default:
            # GH#37982
            warnings.warn(
                "The 'how' keyword in PeriodIndex.astype is deprecated and "
                "will be removed in a future version. "
                "Use index.to_timestamp(how=how) instead.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        else:
            how = "start"

        if is_datetime64_any_dtype(dtype):
            # 'how' is index-specific, isn't part of the EA interface.
            # GH#45038 implement this for PeriodArray (but without "how")
            #  once the "how" deprecation is enforced we can just dispatch
            #  directly to PeriodArray.
            tz = getattr(dtype, "tz", None)
            return self.to_timestamp(how=how).tz_localize(tz)

        return super().astype(dtype, copy=copy)

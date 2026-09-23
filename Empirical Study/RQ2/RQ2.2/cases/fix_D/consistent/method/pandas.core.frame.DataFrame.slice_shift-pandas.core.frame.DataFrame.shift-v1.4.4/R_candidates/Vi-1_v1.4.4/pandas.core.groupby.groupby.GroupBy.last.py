    @final
    @doc(_groupby_agg_method_template, fname="last", no=False, mc=-1)
    def last(self, numeric_only: bool = False, min_count: int = -1):
        def last_compat(obj: NDFrameT, axis: int = 0):
            def last(x: Series):
                """Helper function for last item that isn't NA."""
                arr = x.array[notna(x.array)]
                if not len(arr):
                    return np.nan
                return arr[-1]

            if isinstance(obj, DataFrame):
                return obj.apply(last, axis=axis)
            elif isinstance(obj, Series):
                return last(obj)
            else:  # pragma: no cover
                raise TypeError(type(obj))

        return self._agg_general(
            numeric_only=numeric_only,
            min_count=min_count,
            alias="last",
            npfunc=last_compat,
        )

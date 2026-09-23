    @final
    @doc(_groupby_agg_method_template, fname="first", no=False, mc=-1)
    def first(self, numeric_only: bool = False, min_count: int = -1):
        def first_compat(obj: NDFrameT, axis: int = 0):
            def first(x: Series):
                """Helper function for first item that isn't NA."""
                arr = x.array[notna(x.array)]
                if not len(arr):
                    return np.nan
                return arr[0]

            if isinstance(obj, DataFrame):
                return obj.apply(first, axis=axis)
            elif isinstance(obj, Series):
                return first(obj)
            else:  # pragma: no cover
                raise TypeError(type(obj))

        return self._agg_general(
            numeric_only=numeric_only,
            min_count=min_count,
            alias="first",
            npfunc=first_compat,
        )

    def apply_standard(self) -> DataFrame | Series:
        # caller is responsible for ensuring that f is Callable
        func = cast(Callable, self.func)
        obj = self.obj

        if isinstance(func, np.ufunc):
            with np.errstate(all="ignore"):
                return func(obj, *self.args, **self.kwargs)
        elif not self.by_row:
            return func(obj, *self.args, **self.kwargs)

        if self.args or self.kwargs:
            # _map_values does not support args/kwargs
            def curried(x):
                return func(x, *self.args, **self.kwargs)

        else:
            curried = func

        # row-wise access
        # apply doesn't have a `na_action` keyword and for backward compat reasons
        # we need to give `na_action="ignore"` for categorical data.
        # TODO: remove the `na_action="ignore"` when that default has been changed in
        #  Categorical (GH51645).
        action = "ignore" if isinstance(obj.dtype, CategoricalDtype) else None
        mapped = obj._map_values(
            mapper=curried, na_action=action, convert=self.convert_dtype
        )

        if len(mapped) and isinstance(mapped[0], ABCSeries):
            warnings.warn(
                "Returning a DataFrame from Series.apply when the supplied function "
                "returns a Series is deprecated and will be removed in a future "
                "version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )  # GH52116

            # GH#43986 Need to do list(mapped) in order to get treated as nested
            #  See also GH#25959 regarding EA support
            return obj._constructor_expanddim(list(mapped), index=obj.index)
        else:
            return obj._constructor(mapped, index=obj.index).__finalize__(
                obj, method="apply"
            )

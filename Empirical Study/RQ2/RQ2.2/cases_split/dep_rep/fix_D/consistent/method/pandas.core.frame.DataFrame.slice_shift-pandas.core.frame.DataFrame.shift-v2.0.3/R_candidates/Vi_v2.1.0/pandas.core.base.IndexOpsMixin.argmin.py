    @doc(argmax, op="min", oppose="max", value="smallest")
    def argmin(
        self, axis: AxisInt | None = None, skipna: bool = True, *args, **kwargs
    ) -> int:
        delegate = self._values
        nv.validate_minmax_axis(axis)
        skipna = nv.validate_argmin_with_skipna(skipna, args, kwargs)

        if isinstance(delegate, ExtensionArray):
            if not skipna and delegate.isna().any():
                warnings.warn(
                    f"The behavior of {type(self).__name__}.argmax/argmin "
                    "with skipna=False and NAs, or with all-NAs is deprecated. "
                    "In a future version this will raise ValueError.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
                return -1
            else:
                return delegate.argmin()
        else:
            result = nanops.nanargmin(delegate, skipna=skipna)
            if result == -1:
                warnings.warn(
                    f"The behavior of {type(self).__name__}.argmax/argmin "
                    "with skipna=False and NAs, or with all-NAs is deprecated. "
                    "In a future version this will raise ValueError.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            # error: Incompatible return value type (got "Union[int, ndarray]", expected
            # "int")
            return result  # type: ignore[return-value]

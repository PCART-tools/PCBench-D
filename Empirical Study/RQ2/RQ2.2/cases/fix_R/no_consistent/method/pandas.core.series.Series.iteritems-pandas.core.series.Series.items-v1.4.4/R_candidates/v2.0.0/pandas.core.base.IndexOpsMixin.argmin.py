    @doc(argmax, op="min", oppose="max", value="smallest")
    def argmin(
        self, axis: AxisInt | None = None, skipna: bool = True, *args, **kwargs
    ) -> int:
        delegate = self._values
        nv.validate_minmax_axis(axis)
        skipna = nv.validate_argmin_with_skipna(skipna, args, kwargs)

        if isinstance(delegate, ExtensionArray):
            if not skipna and delegate.isna().any():
                return -1
            else:
                return delegate.argmin()
        else:
            # error: Incompatible return value type (got "Union[int, ndarray]", expected
            # "int")
            return nanops.nanargmin(  # type: ignore[return-value]
                delegate, skipna=skipna
            )

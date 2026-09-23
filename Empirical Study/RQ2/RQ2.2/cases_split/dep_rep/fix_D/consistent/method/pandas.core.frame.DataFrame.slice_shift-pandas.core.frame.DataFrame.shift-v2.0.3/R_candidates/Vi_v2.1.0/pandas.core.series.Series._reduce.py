    def _reduce(
        self,
        op,
        # error: Variable "pandas.core.series.Series.str" is not valid as a type
        name: str,  # type: ignore[valid-type]
        *,
        axis: Axis = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        filter_type=None,
        **kwds,
    ):
        """
        Perform a reduction operation.

        If we have an ndarray as a value, then simply perform the operation,
        otherwise delegate to the object.
        """
        delegate = self._values

        if axis is not None:
            self._get_axis_number(axis)

        if isinstance(delegate, ExtensionArray):
            # dispatch to ExtensionArray interface
            return delegate._reduce(name, skipna=skipna, **kwds)

        else:
            # dispatch to numpy arrays
            if numeric_only and self.dtype.kind not in "iufcb":
                # i.e. not is_numeric_dtype(self.dtype)
                kwd_name = "numeric_only"
                if name in ["any", "all"]:
                    kwd_name = "bool_only"
                # GH#47500 - change to TypeError to match other methods
                raise TypeError(
                    f"Series.{name} does not allow {kwd_name}={numeric_only} "
                    "with non-numeric dtypes."
                )
            return op(delegate, skipna=skipna, **kwds)

    def _reduce(
        self,
        op,
        name: str,
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
            if numeric_only and not is_numeric_dtype(self.dtype):
                kwd_name = "numeric_only"
                if name in ["any", "all"]:
                    kwd_name = "bool_only"
                # GH#47500 - change to TypeError to match other methods
                raise TypeError(
                    f"Series.{name} does not allow {kwd_name}={numeric_only} "
                    "with non-numeric dtypes."
                )
            with np.errstate(all="ignore"):
                return op(delegate, skipna=skipna, **kwds)

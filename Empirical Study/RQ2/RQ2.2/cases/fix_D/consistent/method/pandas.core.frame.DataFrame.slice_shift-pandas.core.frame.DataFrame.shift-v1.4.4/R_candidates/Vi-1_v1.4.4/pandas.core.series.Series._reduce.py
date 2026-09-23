    def _reduce(
        self,
        op,
        name: str,
        *,
        axis=0,
        skipna=True,
        numeric_only=None,
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
            if numeric_only:
                kwd_name = "numeric_only"
                if name in ["any", "all"]:
                    kwd_name = "bool_only"
                raise NotImplementedError(
                    f"Series.{name} does not implement {kwd_name}."
                )
            with np.errstate(all="ignore"):
                return op(delegate, skipna=skipna, **kwds)

    @Appender(make_doc("any", ndim=1))
    # error: Signature of "any" incompatible with supertype "NDFrame"
    def any(  # type: ignore[override]
        self,
        *,
        axis: Axis = 0,
        bool_only: bool = False,
        skipna: bool = True,
        **kwargs,
    ) -> bool:
        nv.validate_logical_func((), kwargs, fname="any")
        validate_bool_kwarg(skipna, "skipna", none_allowed=False)
        return self._reduce(
            nanops.nanany,
            name="any",
            axis=axis,
            numeric_only=bool_only,
            skipna=skipna,
            filter_type="bool",
        )

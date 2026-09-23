    @final
    def _logical_func(
        self,
        name: str,
        func,
        axis: Axis = 0,
        bool_only: bool_t | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        **kwargs,
    ) -> Series | bool_t:
        nv.validate_logical_func((), kwargs, fname=name)
        validate_bool_kwarg(skipna, "skipna", none_allowed=False)
        if level is not None:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. df.any(level=1) should use df.groupby(level=1).any()",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            if bool_only is not None:
                raise NotImplementedError(
                    "Option bool_only is not implemented with option level."
                )
            return self._agg_by_level(name, axis=axis, level=level, skipna=skipna)

        if self.ndim > 1 and axis is None:
            # Reduce along one dimension then the other, to simplify DataFrame._reduce
            res = self._logical_func(
                name, func, axis=0, bool_only=bool_only, skipna=skipna, **kwargs
            )
            return res._logical_func(name, func, skipna=skipna, **kwargs)

        if (
            self.ndim > 1
            and axis == 1
            and len(self._mgr.arrays) > 1
            # TODO(EA2D): special-case not needed
            and all(x.ndim == 2 for x in self._mgr.arrays)
            and bool_only is not None
            and not kwargs
        ):
            # Fastpath avoiding potentially expensive transpose
            obj = self
            if bool_only:
                obj = self._get_bool_data()
            return obj._reduce_axis1(name, func, skipna=skipna)

        return self._reduce(
            func,
            name=name,
            axis=axis,
            skipna=skipna,
            numeric_only=bool_only,
            filter_type="bool",
        )

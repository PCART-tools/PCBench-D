    @Appender(NDFrame.take.__doc__)
    def take(
        self, indices, axis: Axis = 0, is_copy: bool | None = None, **kwargs
    ) -> Series:
        if is_copy is not None:
            warnings.warn(
                "is_copy is deprecated and will be removed in a future version. "
                "'take' always returns a copy, so there is no need to specify this.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        nv.validate_take((), kwargs)

        indices = ensure_platform_int(indices)
        new_index = self.index.take(indices)
        new_values = self._values.take(indices)

        result = self._constructor(new_values, index=new_index, fastpath=True)
        return result.__finalize__(self, method="take")

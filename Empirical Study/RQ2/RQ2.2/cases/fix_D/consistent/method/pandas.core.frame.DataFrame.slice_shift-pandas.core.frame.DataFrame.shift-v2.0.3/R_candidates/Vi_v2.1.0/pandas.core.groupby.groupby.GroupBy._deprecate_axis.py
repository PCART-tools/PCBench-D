    @final
    def _deprecate_axis(self, axis: int, name: str) -> None:
        if axis == 1:
            warnings.warn(
                f"{type(self).__name__}.{name} with axis=1 is deprecated and "
                "will be removed in a future version. Operate on the un-grouped "
                "DataFrame instead",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            warnings.warn(
                f"The 'axis' keyword in {type(self).__name__}.{name} is deprecated "
                "and will be removed in a future version. "
                "Call without passing 'axis' instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

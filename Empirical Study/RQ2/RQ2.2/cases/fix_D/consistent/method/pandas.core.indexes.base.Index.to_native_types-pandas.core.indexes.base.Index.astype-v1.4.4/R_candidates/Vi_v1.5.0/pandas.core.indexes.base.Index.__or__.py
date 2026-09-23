    @final
    def __or__(self, other):
        warnings.warn(
            "Index.__or__ operating as a set operation is deprecated, "
            "in the future this will be a logical operation matching "
            "Series.__or__.  Use index.union(other) instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.union(other)

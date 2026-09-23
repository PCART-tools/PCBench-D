    @final
    def __and__(self, other):
        warnings.warn(
            "Index.__and__ operating as a set operation is deprecated, "
            "in the future this will be a logical operation matching "
            "Series.__and__.  Use index.intersection(other) instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.intersection(other)

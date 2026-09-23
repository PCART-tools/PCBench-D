    @final
    def __xor__(self, other):
        warnings.warn(
            "Index.__xor__ operating as a set operation is deprecated, "
            "in the future this will be a logical operation matching "
            "Series.__xor__.  Use index.symmetric_difference(other) instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.symmetric_difference(other)

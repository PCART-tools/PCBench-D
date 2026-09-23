    def is_dtype_equal(self, other) -> bool:
        warn(
            "Categorical.is_dtype_equal is deprecated and will be removed "
            "in a future version",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        try:
            return self._categories_match_up_to_permutation(other)
        except (AttributeError, TypeError):
            return False

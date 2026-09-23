    @final
    @property
    def is_monotonic(self) -> bool:
        """
        Alias for is_monotonic_increasing.

        .. deprecated:: 1.5.0
            is_monotonic is deprecated and will be removed in a future version.
            Use is_monotonic_increasing instead.
        """
        warnings.warn(
            "is_monotonic is deprecated and will be removed in a future version. "
            "Use is_monotonic_increasing instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self.is_monotonic_increasing

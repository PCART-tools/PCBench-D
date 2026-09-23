    @property
    def is_datetimelike(self) -> bool:
        warnings.warn(
            "is_datetimelike is deprecated and will be removed in a future version.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self._win_freq_i8 is not None

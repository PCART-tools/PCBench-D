    def validate(self) -> None:
        warnings.warn(
            "validate is deprecated and will be removed in a future version.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return self._validate()

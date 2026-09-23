    @property
    def _AXIS_NUMBERS(self) -> dict[str, int]:
        """.. deprecated:: 1.1.0"""
        warnings.warn(
            "_AXIS_NUMBERS has been deprecated.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        return {"index": 0}

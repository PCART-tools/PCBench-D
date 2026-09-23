    @cache_readonly
    def is_datetimelike(self) -> bool:
        return isinstance(
            self._on, (ABCDatetimeIndex, ABCTimedeltaIndex, ABCPeriodIndex)
        )

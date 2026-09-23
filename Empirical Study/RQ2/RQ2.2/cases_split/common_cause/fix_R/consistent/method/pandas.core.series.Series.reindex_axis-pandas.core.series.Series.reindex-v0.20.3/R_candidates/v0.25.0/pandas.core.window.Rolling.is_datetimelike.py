    @cache_readonly
    def is_datetimelike(self):
        return isinstance(
            self._on, (ABCDatetimeIndex, ABCTimedeltaIndex, ABCPeriodIndex)
        )

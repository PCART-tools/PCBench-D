    @Substitution(klass="PeriodIndex")
    @Appender(_shared_docs["searchsorted"])
    def searchsorted(self, value, side="left", sorter=None):
        if isinstance(value, Period) or value is NaT:
            self._data._check_compatible_with(value)
        elif isinstance(value, str):
            try:
                value = Period(value, freq=self.freq)
            except DateParseError:
                raise KeyError(f"Cannot interpret '{value}' as period")
        elif not isinstance(value, PeriodArray):
            raise TypeError(
                "PeriodIndex.searchsorted requires either a Period or PeriodArray"
            )

        return self._data.searchsorted(value, side=side, sorter=sorter)

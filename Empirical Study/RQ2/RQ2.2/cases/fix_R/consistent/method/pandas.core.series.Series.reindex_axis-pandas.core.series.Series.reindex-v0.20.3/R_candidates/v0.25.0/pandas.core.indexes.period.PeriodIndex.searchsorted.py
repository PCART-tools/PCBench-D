    @Substitution(klass="PeriodIndex")
    @Appender(_shared_docs["searchsorted"])
    def searchsorted(self, value, side="left", sorter=None):
        if isinstance(value, Period):
            if value.freq != self.freq:
                msg = DIFFERENT_FREQ.format(
                    cls=type(self).__name__,
                    own_freq=self.freqstr,
                    other_freq=value.freqstr,
                )
                raise IncompatibleFrequency(msg)
            value = value.ordinal
        elif isinstance(value, str):
            try:
                value = Period(value, freq=self.freq).ordinal
            except DateParseError:
                raise KeyError("Cannot interpret '{}' as period".format(value))

        return self._ndarray_values.searchsorted(value, side=side, sorter=sorter)

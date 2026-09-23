    def to_period(self, freq=None):
        """
        Cast to PeriodIndex at a particular frequency
        """
        from pandas.core.indexes.period import PeriodIndex

        if freq is None:
            freq = self.freqstr or self.inferred_freq

            if freq is None:
                msg = ("You must pass a freq argument as "
                       "current index has none.")
                raise ValueError(msg)

            freq = get_period_alias(freq)

        return PeriodIndex(self.values, name=self.name, freq=freq, tz=self.tz)

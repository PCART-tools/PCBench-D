    def to_perioddelta(self, freq) -> TimedeltaArray:
        """
        Calculate TimedeltaArray of difference between index
        values and index converted to PeriodArray at specified
        freq. Used for vectorized offsets.

        Parameters
        ----------
        freq : Period frequency

        Returns
        -------
        TimedeltaArray/Index
        """
        # Deprecaation GH#34853
        warnings.warn(
            "to_perioddelta is deprecated and will be removed in a "
            "future version. "
            "Use `dtindex - dtindex.to_period(freq).to_timestamp()` instead.",
            FutureWarning,
            # stacklevel chosen to be correct for when called from DatetimeIndex
            stacklevel=find_stack_level(),
        )
        from pandas.core.arrays.timedeltas import TimedeltaArray

        i8delta = self.asi8 - self.to_period(freq).to_timestamp().asi8
        m8delta = i8delta.view("m8[ns]")
        return TimedeltaArray(m8delta)

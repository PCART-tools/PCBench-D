    def to_perioddelta(self, freq) -> TimedeltaArray:
        """
        Calculate deltas between self values and self converted to Periods at a freq.

        Used for vectorized offsets.

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
            stacklevel=find_stack_level(inspect.currentframe()),
        )
        from pandas.core.arrays.timedeltas import TimedeltaArray

        if self._ndarray.dtype != "M8[ns]":
            raise NotImplementedError("Only supported for nanosecond resolution.")

        i8delta = self.asi8 - self.to_period(freq).to_timestamp().asi8
        m8delta = i8delta.view("m8[ns]")
        return TimedeltaArray(m8delta)

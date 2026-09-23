    def _add_timedelta_arraylike(self, other: TimedeltaArray):
        """
        Add a delta of a TimedeltaIndex

        Returns
        -------
        Same type as self
        """
        # overridden by PeriodArray

        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        self = cast("DatetimeArray | TimedeltaArray", self)

        self, other = self._ensure_matching_resos(other)
        return self._add_timedeltalike(other)

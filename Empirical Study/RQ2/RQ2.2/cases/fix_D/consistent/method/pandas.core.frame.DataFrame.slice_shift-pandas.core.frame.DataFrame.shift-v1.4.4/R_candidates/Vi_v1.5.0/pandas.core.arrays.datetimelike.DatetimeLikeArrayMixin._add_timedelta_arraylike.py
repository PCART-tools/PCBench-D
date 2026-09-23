    def _add_timedelta_arraylike(
        self, other: TimedeltaArray | npt.NDArray[np.timedelta64]
    ):
        """
        Add a delta of a TimedeltaIndex

        Returns
        -------
        Same type as self
        """
        # overridden by PeriodArray

        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        other = ensure_wrapped_if_datetimelike(other)
        other = cast("TimedeltaArray", other)

        self_i8 = self.asi8
        other_i8 = other.asi8
        new_values = checked_add_with_arr(
            self_i8, other_i8, arr_mask=self._isnan, b_mask=other._isnan
        )
        return type(self)(new_values, dtype=self.dtype)

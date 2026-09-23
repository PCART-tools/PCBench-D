    @final
    def _get_i8_values_and_mask(
        self, other
    ) -> tuple[int | npt.NDArray[np.int64], None | npt.NDArray[np.bool_]]:
        """
        Get the int64 values and b_mask to pass to checked_add_with_arr.
        """
        if isinstance(other, Period):
            i8values = other.ordinal
            mask = None
        elif isinstance(other, (Timestamp, Timedelta)):
            i8values = other._value
            mask = None
        else:
            # PeriodArray, DatetimeArray, TimedeltaArray
            mask = other._isnan
            i8values = other.asi8
        return i8values, mask

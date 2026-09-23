    @final
    def _sub_datetime_arraylike(self, other):
        if self.dtype.kind != "M":
            raise TypeError(f"cannot subtract a datelike from a {type(self).__name__}")

        if len(self) != len(other):
            raise ValueError("cannot add indices of unequal length")

        self = cast("DatetimeArray", self)
        other = ensure_wrapped_if_datetimelike(other)

        try:
            self._assert_tzawareness_compat(other)
        except TypeError as err:
            new_message = str(err).replace("compare", "subtract")
            raise type(err)(new_message) from err

        self_i8 = self.asi8
        other_i8 = other.asi8
        new_values = checked_add_with_arr(
            self_i8, -other_i8, arr_mask=self._isnan, b_mask=other._isnan
        )
        return new_values.view("timedelta64[ns]")

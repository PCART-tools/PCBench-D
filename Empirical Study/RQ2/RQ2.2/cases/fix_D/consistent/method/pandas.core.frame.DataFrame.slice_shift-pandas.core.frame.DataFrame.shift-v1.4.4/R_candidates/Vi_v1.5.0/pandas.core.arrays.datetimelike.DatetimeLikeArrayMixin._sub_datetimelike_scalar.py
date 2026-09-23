    @final
    def _sub_datetimelike_scalar(self, other: datetime | np.datetime64):
        if self.dtype.kind != "M":
            raise TypeError(f"cannot subtract a datelike from a {type(self).__name__}")

        self = cast("DatetimeArray", self)
        # subtract a datetime from myself, yielding a ndarray[timedelta64[ns]]

        # error: Non-overlapping identity check (left operand type: "Union[datetime,
        # datetime64]", right operand type: "NaTType")  [comparison-overlap]
        assert other is not NaT  # type: ignore[comparison-overlap]
        other = Timestamp(other)
        # error: Non-overlapping identity check (left operand type: "Timestamp",
        # right operand type: "NaTType")
        if other is NaT:  # type: ignore[comparison-overlap]
            return self - NaT

        try:
            self._assert_tzawareness_compat(other)
        except TypeError as err:
            new_message = str(err).replace("compare", "subtract")
            raise type(err)(new_message) from err

        i8 = self.asi8
        result = checked_add_with_arr(i8, -other.value, arr_mask=self._isnan)
        return result.view("timedelta64[ns]")

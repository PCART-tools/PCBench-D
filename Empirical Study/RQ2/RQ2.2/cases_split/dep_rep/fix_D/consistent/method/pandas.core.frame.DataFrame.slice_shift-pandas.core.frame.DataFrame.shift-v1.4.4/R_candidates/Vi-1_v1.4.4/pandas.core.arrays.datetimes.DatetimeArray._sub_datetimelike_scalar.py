    def _sub_datetimelike_scalar(self, other):
        # subtract a datetime from myself, yielding a ndarray[timedelta64[ns]]
        assert isinstance(other, (datetime, np.datetime64))
        assert other is not NaT
        other = Timestamp(other)
        # error: Non-overlapping identity check (left operand type: "Timestamp",
        # right operand type: "NaTType")
        if other is NaT:  # type: ignore[comparison-overlap]
            return self - NaT

        try:
            self._assert_tzawareness_compat(other)
        except TypeError as error:
            new_message = str(error).replace("compare", "subtract")
            raise type(error)(new_message) from error

        i8 = self.asi8
        result = checked_add_with_arr(i8, -other.value, arr_mask=self._isnan)
        result = self._maybe_mask_results(result)
        return result.view("timedelta64[ns]")

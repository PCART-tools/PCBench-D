    @final
    def _sub_datetimelike(self, other: Timestamp | DatetimeArray) -> TimedeltaArray:
        self = cast("DatetimeArray", self)

        from pandas.core.arrays import TimedeltaArray

        try:
            self._assert_tzawareness_compat(other)
        except TypeError as err:
            new_message = str(err).replace("compare", "subtract")
            raise type(err)(new_message) from err

        other_i8, o_mask = self._get_i8_values_and_mask(other)
        res_values = checked_add_with_arr(
            self.asi8, -other_i8, arr_mask=self._isnan, b_mask=o_mask
        )
        res_m8 = res_values.view(f"timedelta64[{self.unit}]")

        new_freq = self._get_arithmetic_result_freq(other)
        return TimedeltaArray._simple_new(res_m8, dtype=res_m8.dtype, freq=new_freq)

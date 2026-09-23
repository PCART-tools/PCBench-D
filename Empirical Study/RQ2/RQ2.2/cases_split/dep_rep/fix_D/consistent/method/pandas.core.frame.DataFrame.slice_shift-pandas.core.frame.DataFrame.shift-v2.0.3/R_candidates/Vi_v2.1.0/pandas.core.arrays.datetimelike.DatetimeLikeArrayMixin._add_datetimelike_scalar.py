    @final
    def _add_datetimelike_scalar(self, other) -> DatetimeArray:
        if not lib.is_np_dtype(self.dtype, "m"):
            raise TypeError(
                f"cannot add {type(self).__name__} and {type(other).__name__}"
            )

        self = cast("TimedeltaArray", self)

        from pandas.core.arrays import DatetimeArray
        from pandas.core.arrays.datetimes import tz_to_dtype

        assert other is not NaT
        if isna(other):
            # i.e. np.datetime64("NaT")
            # In this case we specifically interpret NaT as a datetime, not
            # the timedelta interpretation we would get by returning self + NaT
            result = self._ndarray + NaT.to_datetime64().astype(f"M8[{self.unit}]")
            # Preserve our resolution
            return DatetimeArray._simple_new(result, dtype=result.dtype)

        other = Timestamp(other)
        self, other = self._ensure_matching_resos(other)
        self = cast("TimedeltaArray", self)

        other_i8, o_mask = self._get_i8_values_and_mask(other)
        result = checked_add_with_arr(
            self.asi8, other_i8, arr_mask=self._isnan, b_mask=o_mask
        )
        res_values = result.view(f"M8[{self.unit}]")

        dtype = tz_to_dtype(tz=other.tz, unit=self.unit)
        res_values = result.view(f"M8[{self.unit}]")
        new_freq = self._get_arithmetic_result_freq(other)
        return DatetimeArray._simple_new(res_values, dtype=dtype, freq=new_freq)

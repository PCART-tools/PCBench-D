    @final
    def _add_datetimelike_scalar(self, other) -> DatetimeArray:
        if not is_timedelta64_dtype(self.dtype):
            raise TypeError(
                f"cannot add {type(self).__name__} and {type(other).__name__}"
            )

        self = cast("TimedeltaArray", self)

        from pandas.core.arrays import DatetimeArray
        from pandas.core.arrays.datetimes import tz_to_dtype

        assert other is not NaT
        other = Timestamp(other)
        if other is NaT:
            # In this case we specifically interpret NaT as a datetime, not
            # the timedelta interpretation we would get by returning self + NaT
            result = self._ndarray + NaT.to_datetime64().astype(f"M8[{self._unit}]")
            # Preserve our resolution
            return DatetimeArray._simple_new(result, dtype=result.dtype)

        if self._reso != other._reso:
            raise NotImplementedError(
                "Addition between TimedeltaArray and Timestamp with mis-matched "
                "resolutions is not yet supported."
            )

        i8 = self.asi8
        result = checked_add_with_arr(i8, other.value, arr_mask=self._isnan)
        dtype = tz_to_dtype(tz=other.tz, unit=self._unit)
        res_values = result.view(f"M8[{self._unit}]")
        return DatetimeArray._simple_new(res_values, dtype=dtype, freq=self.freq)

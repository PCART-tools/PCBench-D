    def _get_values(self):
        data = self._parent
        if is_datetime64_dtype(data.dtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif is_datetime64tz_dtype(data.dtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif is_timedelta64_dtype(data.dtype):
            return TimedeltaIndex(data, copy=False, name=self.name)

        else:
            if is_period_arraylike(data):
                # TODO: use to_period_array
                return PeriodArray(data, copy=False)
            if is_datetime_arraylike(data):
                return DatetimeIndex(data, copy=False, name=self.name)

        raise TypeError(
            f"cannot convert an object of type {type(data)} to a datetimelike index"
        )

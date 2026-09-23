    def _get_values(self):
        data = self.values
        if is_datetime64_dtype(data.dtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif is_datetime64tz_dtype(data.dtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif is_timedelta64_dtype(data.dtype):
            return TimedeltaIndex(data, copy=False, name=self.name)

        else:
            if is_period_arraylike(data):
                return PeriodIndex(data, copy=False, name=self.name)
            if is_datetime_arraylike(data):
                return DatetimeIndex(data, copy=False, name=self.name)

        raise TypeError("cannot convert an object of type {0} to a "
                        "datetimelike index".format(type(data)))

    def __new__(cls, data):
        # CombinedDatetimelikeProperties isn't really instantiated. Instead
        # we need to choose which parent (datetime or timedelta) is
        # appropriate. Since we're checking the dtypes anyway, we'll just
        # do all the validation here.
        from pandas import Series

        if not isinstance(data, ABCSeries):
            raise TypeError(
                f"cannot convert an object of type {type(data)} to a datetimelike index"
            )

        orig = data if is_categorical_dtype(data) else None
        if orig is not None:
            data = Series(
                orig.array,
                name=orig.name,
                copy=False,
                dtype=orig.values.categories.dtype,
            )

        if is_datetime64_dtype(data.dtype):
            return DatetimeProperties(data, orig)
        elif is_datetime64tz_dtype(data.dtype):
            return DatetimeProperties(data, orig)
        elif is_timedelta64_dtype(data.dtype):
            return TimedeltaProperties(data, orig)
        elif is_period_arraylike(data):
            return PeriodProperties(data, orig)
        elif is_datetime_arraylike(data):
            return DatetimeProperties(data, orig)

        raise AttributeError("Can only use .dt accessor with datetimelike values")

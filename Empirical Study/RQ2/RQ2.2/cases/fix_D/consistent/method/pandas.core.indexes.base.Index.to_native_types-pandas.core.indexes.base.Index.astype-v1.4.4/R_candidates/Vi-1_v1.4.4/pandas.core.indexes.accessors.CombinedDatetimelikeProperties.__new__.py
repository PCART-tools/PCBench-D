    def __new__(cls, data: Series):
        # CombinedDatetimelikeProperties isn't really instantiated. Instead
        # we need to choose which parent (datetime or timedelta) is
        # appropriate. Since we're checking the dtypes anyway, we'll just
        # do all the validation here.

        if not isinstance(data, ABCSeries):
            raise TypeError(
                f"cannot convert an object of type {type(data)} to a datetimelike index"
            )

        orig = data if is_categorical_dtype(data.dtype) else None
        if orig is not None:
            data = data._constructor(
                orig.array,
                name=orig.name,
                copy=False,
                dtype=orig._values.categories.dtype,
                index=orig.index,
            )

        if is_datetime64_dtype(data.dtype):
            return DatetimeProperties(data, orig)
        elif is_datetime64tz_dtype(data.dtype):
            return DatetimeProperties(data, orig)
        elif is_timedelta64_dtype(data.dtype):
            return TimedeltaProperties(data, orig)
        elif is_period_dtype(data.dtype):
            return PeriodProperties(data, orig)

        raise AttributeError("Can only use .dt accessor with datetimelike values")

    def __new__(cls, data):
        # CombinedDatetimelikeProperties isn't really instantiated. Instead
        # we need to choose which parent (datetime or timedelta) is
        # appropriate. Since we're checking the dtypes anyway, we'll just
        # do all the validation here.
        from pandas import Series

        if not isinstance(data, Series):
            raise TypeError("cannot convert an object of type {0} to a "
                            "datetimelike index".format(type(data)))

        orig = data if is_categorical_dtype(data) else None
        if orig is not None:
            data = Series(orig.values.categories,
                          name=orig.name,
                          copy=False)

        try:
            if is_datetime64_dtype(data.dtype):
                return DatetimeProperties(data, orig)
            elif is_datetime64tz_dtype(data.dtype):
                return DatetimeProperties(data, orig)
            elif is_timedelta64_dtype(data.dtype):
                return TimedeltaProperties(data, orig)
            else:
                if is_period_arraylike(data):
                    return PeriodProperties(data, orig)
                if is_datetime_arraylike(data):
                    return DatetimeProperties(data, orig)
        except Exception:
            pass  # we raise an attribute error anyway

        raise AttributeError("Can only use .dt accessor with datetimelike "
                             "values")

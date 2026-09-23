    def __new__(cls, data: Series):  # pyright: ignore[reportInconsistentConstructor]
        # CombinedDatetimelikeProperties isn't really instantiated. Instead
        # we need to choose which parent (datetime or timedelta) is
        # appropriate. Since we're checking the dtypes anyway, we'll just
        # do all the validation here.

        if not isinstance(data, ABCSeries):
            raise TypeError(
                f"cannot convert an object of type {type(data)} to a datetimelike index"
            )

        orig = data if isinstance(data.dtype, CategoricalDtype) else None
        if orig is not None:
            data = data._constructor(
                orig.array,
                name=orig.name,
                copy=False,
                dtype=orig._values.categories.dtype,
                index=orig.index,
            )

        if isinstance(data.dtype, ArrowDtype) and data.dtype.kind == "M":
            return ArrowTemporalProperties(data, orig)
        if lib.is_np_dtype(data.dtype, "M"):
            return DatetimeProperties(data, orig)
        elif isinstance(data.dtype, DatetimeTZDtype):
            return DatetimeProperties(data, orig)
        elif lib.is_np_dtype(data.dtype, "m"):
            return TimedeltaProperties(data, orig)
        elif isinstance(data.dtype, PeriodDtype):
            return PeriodProperties(data, orig)

        raise AttributeError("Can only use .dt accessor with datetimelike values")

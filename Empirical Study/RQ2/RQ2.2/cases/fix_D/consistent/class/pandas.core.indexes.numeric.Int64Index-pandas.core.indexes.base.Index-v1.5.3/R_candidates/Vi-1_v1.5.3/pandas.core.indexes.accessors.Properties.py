class Properties(PandasDelegate, PandasObject, NoNewAttributesMixin):
    _hidden_attrs = PandasObject._hidden_attrs | {
        "orig",
        "name",
    }

    def __init__(self, data: Series, orig) -> None:
        if not isinstance(data, ABCSeries):
            raise TypeError(
                f"cannot convert an object of type {type(data)} to a datetimelike index"
            )

        self._parent = data
        self.orig = orig
        self.name = getattr(data, "name", None)
        self._freeze()

    def _get_values(self):
        data = self._parent
        if is_datetime64_dtype(data.dtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif is_datetime64tz_dtype(data.dtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif is_timedelta64_dtype(data.dtype):
            return TimedeltaIndex(data, copy=False, name=self.name)

        elif is_period_dtype(data.dtype):
            return PeriodArray(data, copy=False)

        raise TypeError(
            f"cannot convert an object of type {type(data)} to a datetimelike index"
        )

    def _delegate_property_get(self, name):
        from pandas import Series

        values = self._get_values()

        result = getattr(values, name)

        # maybe need to upcast (ints)
        if isinstance(result, np.ndarray):
            if is_integer_dtype(result):
                result = result.astype("int64")
        elif not is_list_like(result):
            return result

        result = np.asarray(result)

        if self.orig is not None:
            index = self.orig.index
        else:
            index = self._parent.index
        # return the result as a Series, which is by definition a copy
        result = Series(result, index=index, name=self.name).__finalize__(self._parent)

        # setting this object will show a SettingWithCopyWarning/Error
        result._is_copy = (
            "modifications to a property of a datetimelike "
            "object are not supported and are discarded. "
            "Change values on the original."
        )

        return result

    def _delegate_property_set(self, name, value, *args, **kwargs):
        raise ValueError(
            "modifications to a property of a datetimelike object are not supported. "
            "Change values on the original."
        )

    def _delegate_method(self, name, *args, **kwargs):
        from pandas import Series

        values = self._get_values()

        method = getattr(values, name)
        result = method(*args, **kwargs)

        if not is_list_like(result):
            return result

        result = Series(result, index=self._parent.index, name=self.name).__finalize__(
            self._parent
        )

        # setting this object will show a SettingWithCopyWarning/Error
        result._is_copy = (
            "modifications to a method of a datetimelike "
            "object are not supported and are discarded. "
            "Change values on the original."
        )

        return result

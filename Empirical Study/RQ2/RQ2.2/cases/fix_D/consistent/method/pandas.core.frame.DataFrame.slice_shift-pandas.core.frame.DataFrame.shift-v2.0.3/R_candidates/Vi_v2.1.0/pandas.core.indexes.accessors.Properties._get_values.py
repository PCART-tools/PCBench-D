    def _get_values(self):
        data = self._parent
        if lib.is_np_dtype(data.dtype, "M"):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif isinstance(data.dtype, DatetimeTZDtype):
            return DatetimeIndex(data, copy=False, name=self.name)

        elif lib.is_np_dtype(data.dtype, "m"):
            return TimedeltaIndex(data, copy=False, name=self.name)

        elif isinstance(data.dtype, PeriodDtype):
            return PeriodArray(data, copy=False)

        raise TypeError(
            f"cannot convert an object of type {type(data)} to a datetimelike index"
        )

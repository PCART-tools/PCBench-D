    @unpack_zerodim_and_defer("__add__")
    def __add__(self, other):
        other_dtype = getattr(other, "dtype", None)
        other = ensure_wrapped_if_datetimelike(other)

        # scalar others
        if other is NaT:
            result = self._add_nat()
        elif isinstance(other, (Tick, timedelta, np.timedelta64)):
            result = self._add_timedeltalike_scalar(other)
        elif isinstance(other, BaseOffset):
            # specifically _not_ a Tick
            result = self._add_offset(other)
        elif isinstance(other, (datetime, np.datetime64)):
            result = self._add_datetimelike_scalar(other)
        elif isinstance(other, Period) and is_timedelta64_dtype(self.dtype):
            result = self._add_period(other)
        elif lib.is_integer(other):
            # This check must come after the check for np.timedelta64
            # as is_integer returns True for these
            if not is_period_dtype(self.dtype):
                raise integer_op_not_supported(self)
            obj = cast("PeriodArray", self)
            result = obj._addsub_int_array_or_scalar(other * obj.freq.n, operator.add)

        # array-like others
        elif is_timedelta64_dtype(other_dtype):
            # TimedeltaIndex, ndarray[timedelta64]
            result = self._add_timedelta_arraylike(other)
        elif is_object_dtype(other_dtype):
            # e.g. Array/Index of DateOffset objects
            result = self._addsub_object_array(other, operator.add)
        elif is_datetime64_dtype(other_dtype) or is_datetime64tz_dtype(other_dtype):
            # DatetimeIndex, ndarray[datetime64]
            return self._add_datetime_arraylike(other)
        elif is_integer_dtype(other_dtype):
            if not is_period_dtype(self.dtype):
                raise integer_op_not_supported(self)
            obj = cast("PeriodArray", self)
            result = obj._addsub_int_array_or_scalar(other * obj.freq.n, operator.add)
        else:
            # Includes Categorical, other ExtensionArrays
            # For PeriodDtype, if self is a TimedeltaArray and other is a
            #  PeriodArray with  a timedelta-like (i.e. Tick) freq, this
            #  operation is valid.  Defer to the PeriodArray implementation.
            #  In remaining cases, this will end up raising TypeError.
            return NotImplemented

        if isinstance(result, np.ndarray) and is_timedelta64_dtype(result.dtype):
            from pandas.core.arrays import TimedeltaArray

            return TimedeltaArray(result)
        return result

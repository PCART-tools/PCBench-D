    def __add__(self, other):
        other = lib.item_from_zerodim(other)
        if isinstance(other, (ABCSeries, ABCDataFrame)):
            return NotImplemented

        # scalar others
        elif other is NaT:
            result = self._add_nat()
        elif isinstance(other, (Tick, timedelta, np.timedelta64)):
            result = self._add_delta(other)
        elif isinstance(other, DateOffset):
            # specifically _not_ a Tick
            result = self._add_offset(other)
        elif isinstance(other, (datetime, np.datetime64)):
            result = self._add_datetimelike_scalar(other)
        elif lib.is_integer(other):
            # This check must come after the check for np.timedelta64
            # as is_integer returns True for these
            if not is_period_dtype(self):
                maybe_integer_op_deprecated(self)
            result = self._time_shift(other)

        # array-like others
        elif is_timedelta64_dtype(other):
            # TimedeltaIndex, ndarray[timedelta64]
            result = self._add_delta(other)
        elif is_offsetlike(other):
            # Array/Index of DateOffset objects
            result = self._addsub_offset_array(other, operator.add)
        elif is_datetime64_dtype(other) or is_datetime64tz_dtype(other):
            # DatetimeIndex, ndarray[datetime64]
            return self._add_datetime_arraylike(other)
        elif is_integer_dtype(other):
            if not is_period_dtype(self):
                maybe_integer_op_deprecated(self)
            result = self._addsub_int_array(other, operator.add)
        elif is_float_dtype(other):
            # Explicitly catch invalid dtypes
            raise TypeError("cannot add {dtype}-dtype to {cls}"
                            .format(dtype=other.dtype,
                                    cls=type(self).__name__))
        elif is_period_dtype(other):
            # if self is a TimedeltaArray and other is a PeriodArray with
            #  a timedelta-like (i.e. Tick) freq, this operation is valid.
            #  Defer to the PeriodArray implementation.
            # In remaining cases, this will end up raising TypeError.
            return NotImplemented
        elif is_extension_array_dtype(other):
            # Categorical op will raise; defer explicitly
            return NotImplemented
        else:  # pragma: no cover
            return NotImplemented

        if is_timedelta64_dtype(result) and isinstance(result, np.ndarray):
            from pandas.core.arrays import TimedeltaArray
            # TODO: infer freq?
            return TimedeltaArray(result)
        return result

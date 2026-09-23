    def __sub__(self, other):
        other = lib.item_from_zerodim(other)
        if isinstance(other, (ABCSeries, ABCDataFrame)):
            return NotImplemented

        # scalar others
        elif other is NaT:
            result = self._sub_nat()
        elif isinstance(other, (Tick, timedelta, np.timedelta64)):
            result = self._add_delta(-other)
        elif isinstance(other, DateOffset):
            # specifically _not_ a Tick
            result = self._add_offset(-other)
        elif isinstance(other, (datetime, np.datetime64)):
            result = self._sub_datetimelike_scalar(other)
        elif lib.is_integer(other):
            # This check must come after the check for np.timedelta64
            # as is_integer returns True for these
            if not is_period_dtype(self):
                maybe_integer_op_deprecated(self)
            result = self._time_shift(-other)

        elif isinstance(other, Period):
            result = self._sub_period(other)

        # array-like others
        elif is_timedelta64_dtype(other):
            # TimedeltaIndex, ndarray[timedelta64]
            result = self._add_delta(-other)
        elif is_offsetlike(other):
            # Array/Index of DateOffset objects
            result = self._addsub_offset_array(other, operator.sub)
        elif is_datetime64_dtype(other) or is_datetime64tz_dtype(other):
            # DatetimeIndex, ndarray[datetime64]
            result = self._sub_datetime_arraylike(other)
        elif is_period_dtype(other):
            # PeriodIndex
            result = self._sub_period_array(other)
        elif is_integer_dtype(other):
            if not is_period_dtype(self):
                maybe_integer_op_deprecated(self)
            result = self._addsub_int_array(other, operator.sub)
        elif isinstance(other, ABCIndexClass):
            raise TypeError("cannot subtract {cls} and {typ}"
                            .format(cls=type(self).__name__,
                                    typ=type(other).__name__))
        elif is_float_dtype(other):
            # Explicitly catch invalid dtypes
            raise TypeError("cannot subtract {dtype}-dtype from {cls}"
                            .format(dtype=other.dtype,
                                    cls=type(self).__name__))
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

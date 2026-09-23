    @classmethod
    def _add_datetimelike_methods(cls):
        """
        add in the datetimelike methods (as we may have to override the
        superclass)
        """

        def __add__(self, other):
            from pandas import DateOffset

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
                result = self._add_datelike(other)
            elif is_integer(other):
                # This check must come after the check for np.timedelta64
                # as is_integer returns True for these
                result = self.shift(other)

            # array-like others
            elif is_timedelta64_dtype(other):
                # TimedeltaIndex, ndarray[timedelta64]
                result = self._add_delta(other)
            elif is_offsetlike(other):
                # Array/Index of DateOffset objects
                result = self._addsub_offset_array(other, operator.add)
            elif is_datetime64_dtype(other) or is_datetime64tz_dtype(other):
                # DatetimeIndex, ndarray[datetime64]
                return self._add_datelike(other)
            elif is_integer_dtype(other) and self.freq is None:
                # GH#19123
                raise NullFrequencyError("Cannot shift with no freq")
            elif is_float_dtype(other):
                # Explicitly catch invalid dtypes
                raise TypeError("cannot add {dtype}-dtype to {cls}"
                                .format(dtype=other.dtype,
                                        cls=type(self).__name__))

            else:  # pragma: no cover
                return NotImplemented

            if result is NotImplemented:
                return NotImplemented
            elif not isinstance(result, Index):
                # Index.__new__ will choose appropriate subclass for dtype
                result = Index(result)
            res_name = ops.get_op_result_name(self, other)
            result.name = res_name
            return result

        cls.__add__ = __add__

        def __radd__(self, other):
            # alias for __add__
            return self.__add__(other)
        cls.__radd__ = __radd__

        def __sub__(self, other):
            from pandas import Index

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
                result = self._sub_datelike(other)
            elif is_integer(other):
                # This check must come after the check for np.timedelta64
                # as is_integer returns True for these
                result = self.shift(-other)
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
                result = self._sub_datelike(other)
            elif isinstance(other, Index):
                raise TypeError("cannot subtract {cls} and {typ}"
                                .format(cls=type(self).__name__,
                                        typ=type(other).__name__))
            elif is_integer_dtype(other) and self.freq is None:
                # GH#19123
                raise NullFrequencyError("Cannot shift with no freq")

            elif is_float_dtype(other):
                # Explicitly catch invalid dtypes
                raise TypeError("cannot subtract {dtype}-dtype from {cls}"
                                .format(dtype=other.dtype,
                                        cls=type(self).__name__))
            else:  # pragma: no cover
                return NotImplemented

            if result is NotImplemented:
                return NotImplemented
            elif not isinstance(result, Index):
                # Index.__new__ will choose appropriate subclass for dtype
                result = Index(result)
            res_name = ops.get_op_result_name(self, other)
            result.name = res_name
            return result

        cls.__sub__ = __sub__

        def __rsub__(self, other):
            if is_datetime64_dtype(other) and is_timedelta64_dtype(self):
                # ndarray[datetime64] cannot be subtracted from self, so
                # we need to wrap in DatetimeIndex and flip the operation
                from pandas import DatetimeIndex
                return DatetimeIndex(other) - self
            return -(self - other)
        cls.__rsub__ = __rsub__

        def __iadd__(self, other):
            # alias for __add__
            return self.__add__(other)
        cls.__iadd__ = __iadd__

        def __isub__(self, other):
            # alias for __sub__
            return self.__sub__(other)
        cls.__isub__ = __isub__

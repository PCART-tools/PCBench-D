    def astype(self, dtype, copy: bool = True):
        # Some notes on cases we don't have to handle here in the base class:
        #   1. PeriodArray.astype handles period -> period
        #   2. DatetimeArray.astype handles conversion between tz.
        #   3. DatetimeArray.astype handles datetime -> period
        dtype = pandas_dtype(dtype)

        if is_object_dtype(dtype):
            if self.dtype.kind == "M":
                self = cast("DatetimeArray", self)
                # *much* faster than self._box_values
                #  for e.g. test_get_loc_tuple_monotonic_above_size_cutoff
                i8data = self.asi8
                converted = ints_to_pydatetime(
                    i8data,
                    tz=self.tz,
                    freq=self.freq,
                    box="timestamp",
                    reso=self._reso,
                )
                return converted

            elif self.dtype.kind == "m":
                return ints_to_pytimedelta(self._ndarray, box=True)

            return self._box_values(self.asi8.ravel()).reshape(self.shape)

        elif isinstance(dtype, ExtensionDtype):
            return super().astype(dtype, copy=copy)
        elif is_string_dtype(dtype):
            return self._format_native_types()
        elif is_integer_dtype(dtype):
            # we deliberately ignore int32 vs. int64 here.
            # See https://github.com/pandas-dev/pandas/issues/24381 for more.
            values = self.asi8

            if is_unsigned_integer_dtype(dtype):
                # Again, we ignore int32 vs. int64
                values = values.view("uint64")
                if dtype != np.uint64:
                    # GH#45034
                    warnings.warn(
                        f"The behavior of .astype from {self.dtype} to {dtype} is "
                        "deprecated. In a future version, this astype will return "
                        "exactly the specified dtype instead of uint64, and will "
                        "raise if that conversion overflows.",
                        FutureWarning,
                        stacklevel=find_stack_level(inspect.currentframe()),
                    )
                elif (self.asi8 < 0).any():
                    # GH#45034
                    warnings.warn(
                        f"The behavior of .astype from {self.dtype} to {dtype} is "
                        "deprecated. In a future version, this astype will "
                        "raise if the conversion overflows, as it did in this "
                        "case with negative int64 values.",
                        FutureWarning,
                        stacklevel=find_stack_level(inspect.currentframe()),
                    )
            elif dtype != np.int64:
                # GH#45034
                warnings.warn(
                    f"The behavior of .astype from {self.dtype} to {dtype} is "
                    "deprecated. In a future version, this astype will return "
                    "exactly the specified dtype instead of int64, and will "
                    "raise if that conversion overflows.",
                    FutureWarning,
                    stacklevel=find_stack_level(inspect.currentframe()),
                )

            if copy:
                values = values.copy()
            return values
        elif (
            is_datetime_or_timedelta_dtype(dtype)
            and not is_dtype_equal(self.dtype, dtype)
        ) or is_float_dtype(dtype):
            # disallow conversion between datetime/timedelta,
            # and conversions for any datetimelike to float
            msg = f"Cannot cast {type(self).__name__} to dtype {dtype}"
            raise TypeError(msg)
        else:
            return np.asarray(self, dtype=dtype)

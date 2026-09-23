    def astype(self, dtype, copy: bool = True):
        # Some notes on cases we don't have to handle here in the base class:
        #   1. PeriodArray.astype handles period -> period
        #   2. DatetimeArray.astype handles conversion between tz.
        #   3. DatetimeArray.astype handles datetime -> period
        dtype = pandas_dtype(dtype)

        if dtype == object:
            if self.dtype.kind == "M":
                self = cast("DatetimeArray", self)
                # *much* faster than self._box_values
                #  for e.g. test_get_loc_tuple_monotonic_above_size_cutoff
                i8data = self.asi8
                converted = ints_to_pydatetime(
                    i8data,
                    tz=self.tz,
                    box="timestamp",
                    reso=self._creso,
                )
                return converted

            elif self.dtype.kind == "m":
                return ints_to_pytimedelta(self._ndarray, box=True)

            return self._box_values(self.asi8.ravel()).reshape(self.shape)

        elif isinstance(dtype, ExtensionDtype):
            return super().astype(dtype, copy=copy)
        elif is_string_dtype(dtype):
            return self._format_native_types()
        elif dtype.kind in "iu":
            # we deliberately ignore int32 vs. int64 here.
            # See https://github.com/pandas-dev/pandas/issues/24381 for more.
            values = self.asi8
            if dtype != np.int64:
                raise TypeError(
                    f"Converting from {self.dtype} to {dtype} is not supported. "
                    "Do obj.astype('int64').astype(dtype) instead"
                )

            if copy:
                values = values.copy()
            return values
        elif (dtype.kind in "mM" and self.dtype != dtype) or dtype.kind == "f":
            # disallow conversion between datetime/timedelta,
            # and conversions for any datetimelike to float
            msg = f"Cannot cast {type(self).__name__} to dtype {dtype}"
            raise TypeError(msg)
        else:
            return np.asarray(self, dtype=dtype)

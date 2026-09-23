    def astype(self, dtype, copy: bool = True):
        # We handle
        #   --> datetime
        #   --> period
        # DatetimeLikeArrayMixin Super handles the rest.
        dtype = pandas_dtype(dtype)

        if is_dtype_equal(dtype, self.dtype):
            if copy:
                return self.copy()
            return self

        elif (
            self.tz is None
            and is_datetime64_dtype(dtype)
            and not is_unitless(dtype)
            and is_supported_unit(get_unit_from_dtype(dtype))
        ):
            # unit conversion e.g. datetime64[s]
            res_values = astype_overflowsafe(self._ndarray, dtype, copy=True)
            return type(self)._simple_new(res_values, dtype=res_values.dtype)
            # TODO: preserve freq?

        elif is_datetime64_ns_dtype(dtype):
            return astype_dt64_to_dt64tz(self, dtype, copy, via_utc=False)

        elif self.tz is not None and isinstance(dtype, DatetimeTZDtype):
            # tzaware unit conversion e.g. datetime64[s, UTC]
            np_dtype = np.dtype(dtype.str)
            res_values = astype_overflowsafe(self._ndarray, np_dtype, copy=copy)
            return type(self)._simple_new(res_values, dtype=dtype)
            # TODO: preserve freq?

        elif (
            self.tz is None
            and is_datetime64_dtype(dtype)
            and dtype != self.dtype
            and is_unitless(dtype)
        ):
            # TODO(2.0): just fall through to dtl.DatetimeLikeArrayMixin.astype
            warnings.warn(
                "Passing unit-less datetime64 dtype to .astype is deprecated "
                "and will raise in a future version. Pass 'datetime64[ns]' instead",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            # unit conversion e.g. datetime64[s]
            return self._ndarray.astype(dtype)

        elif is_period_dtype(dtype):
            return self.to_period(freq=dtype.freq)
        return dtl.DatetimeLikeArrayMixin.astype(self, dtype, copy)

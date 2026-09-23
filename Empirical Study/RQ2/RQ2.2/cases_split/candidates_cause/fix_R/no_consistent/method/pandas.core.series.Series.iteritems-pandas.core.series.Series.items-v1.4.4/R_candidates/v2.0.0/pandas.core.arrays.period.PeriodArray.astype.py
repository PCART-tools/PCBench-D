    def astype(self, dtype, copy: bool = True):
        # We handle Period[T] -> Period[U]
        # Our parent handles everything else.
        dtype = pandas_dtype(dtype)
        if is_dtype_equal(dtype, self._dtype):
            if not copy:
                return self
            else:
                return self.copy()
        if is_period_dtype(dtype):
            return self.asfreq(dtype.freq)

        if is_datetime64_any_dtype(dtype):
            # GH#45038 match PeriodIndex behavior.
            tz = getattr(dtype, "tz", None)
            return self.to_timestamp().tz_localize(tz)

        return super().astype(dtype, copy=copy)

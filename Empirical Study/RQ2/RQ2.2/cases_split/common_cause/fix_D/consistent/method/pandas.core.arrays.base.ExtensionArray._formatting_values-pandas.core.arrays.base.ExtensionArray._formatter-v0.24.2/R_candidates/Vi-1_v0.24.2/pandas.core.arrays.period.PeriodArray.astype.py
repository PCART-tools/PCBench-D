    def astype(self, dtype, copy=True):
        # We handle Period[T] -> Period[U]
        # Our parent handles everything else.
        dtype = pandas_dtype(dtype)

        if is_period_dtype(dtype):
            return self.asfreq(dtype.freq)
        return super(PeriodArray, self).astype(dtype, copy=copy)

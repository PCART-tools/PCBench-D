    def to_pandas_dtype(self):
        return IntervalDtype(self.subtype.to_pandas_dtype(), self.closed)

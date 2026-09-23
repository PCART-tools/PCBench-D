    def to_pandas_dtype(self):
        return PeriodDtype(freq=self.freq)

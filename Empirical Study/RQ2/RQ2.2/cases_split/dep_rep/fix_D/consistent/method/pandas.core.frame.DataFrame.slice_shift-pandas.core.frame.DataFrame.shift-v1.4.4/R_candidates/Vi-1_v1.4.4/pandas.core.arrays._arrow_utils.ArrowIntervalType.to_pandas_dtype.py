    def to_pandas_dtype(self):
        import pandas as pd

        return pd.IntervalDtype(self.subtype.to_pandas_dtype(), self.closed)

        def to_pandas_dtype(self):
            import pandas as pd

            return pd.PeriodDtype(freq=self.freq)

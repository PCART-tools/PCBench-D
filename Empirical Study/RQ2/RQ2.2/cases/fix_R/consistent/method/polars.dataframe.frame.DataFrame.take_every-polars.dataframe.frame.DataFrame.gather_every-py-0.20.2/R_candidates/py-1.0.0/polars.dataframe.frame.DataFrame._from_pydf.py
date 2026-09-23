    @classmethod
    def _from_pydf(cls, py_df: PyDataFrame) -> DataFrame:
        """Construct Polars DataFrame from FFI PyDataFrame object."""
        df = cls.__new__(cls)
        df._df = py_df
        return df

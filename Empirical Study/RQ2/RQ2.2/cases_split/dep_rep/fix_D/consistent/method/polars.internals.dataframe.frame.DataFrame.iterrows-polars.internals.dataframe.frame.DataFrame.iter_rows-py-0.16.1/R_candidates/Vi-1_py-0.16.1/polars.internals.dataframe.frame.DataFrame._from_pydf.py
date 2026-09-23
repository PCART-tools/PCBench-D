    @classmethod
    def _from_pydf(cls: type[DF], py_df: PyDataFrame) -> DF:
        """Construct Polars DataFrame from FFI PyDataFrame object."""
        df = cls.__new__(cls)
        df._df = py_df
        return df

    @cache_readonly
    def numpy_dtype(self) -> np.dtype:
        """Return an instance of the related numpy dtype"""
        if pa.types.is_string(self.pyarrow_dtype):
            # pa.string().to_pandas_dtype() = object which we don't want
            return np.dtype(str)
        try:
            return np.dtype(self.pyarrow_dtype.to_pandas_dtype())
        except (NotImplementedError, TypeError):
            return np.dtype(object)

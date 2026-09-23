    def astype(self, dtype, copy: bool = True):
        dtype = pandas_dtype(dtype)

        if is_dtype_equal(dtype, self.dtype):
            if copy:
                return self.copy()
            return self

        result = astype_array(self._ndarray, dtype=dtype, copy=copy)
        return result

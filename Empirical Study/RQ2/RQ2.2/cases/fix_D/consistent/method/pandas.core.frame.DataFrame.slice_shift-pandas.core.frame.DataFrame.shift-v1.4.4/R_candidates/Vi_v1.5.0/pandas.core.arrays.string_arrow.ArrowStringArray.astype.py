    def astype(self, dtype, copy: bool = True):
        dtype = pandas_dtype(dtype)

        if is_dtype_equal(dtype, self.dtype):
            if copy:
                return self.copy()
            return self

        elif isinstance(dtype, NumericDtype):
            data = self._data.cast(pa.from_numpy_dtype(dtype.numpy_dtype))
            return dtype.__from_arrow__(data)

        return super().astype(dtype, copy=copy)

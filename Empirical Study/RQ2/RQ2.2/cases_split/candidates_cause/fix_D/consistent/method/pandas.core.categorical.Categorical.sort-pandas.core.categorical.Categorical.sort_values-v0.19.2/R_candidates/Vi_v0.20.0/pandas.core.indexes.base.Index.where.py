    @Appender(_index_shared_docs['where'])
    def where(self, cond, other=None):
        if other is None:
            other = self._na_value
        values = np.where(cond, self.values, other)

        dtype = self.dtype
        if self._is_numeric_dtype and np.any(isnull(values)):
            # We can't coerce to the numeric dtype of "self" (unless
            # it's float) if there are NaN values in our output.
            dtype = None

        return self._shallow_copy_with_infer(values, dtype=dtype)

    @Appender(_index_shared_docs['where'])
    def where(self, cond, other=None):
        if other is None:
            other = self._na_value

        dtype = self.dtype
        values = self.values

        if is_bool(other) or is_bool_dtype(other):

            # bools force casting
            values = values.astype(object)
            dtype = None

        values = np.where(cond, values, other)

        if self._is_numeric_dtype and np.any(isna(values)):
            # We can't coerce to the numeric dtype of "self" (unless
            # it's float) if there are NaN values in our output.
            dtype = None

        return self._shallow_copy_with_infer(values, dtype=dtype)

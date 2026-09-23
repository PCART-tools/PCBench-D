    def _unary_method(self, op) -> SparseArray:
        fill_value = op(np.array(self.fill_value)).item()
        dtype = SparseDtype(self.dtype.subtype, fill_value)
        # NOTE: if fill_value doesn't change
        # we just have to apply op to sp_values
        if isna(self.fill_value) or fill_value == self.fill_value:
            values = op(self.sp_values)
            return type(self)._simple_new(values, self.sp_index, self.dtype)
        # In the other case we have to recalc indexes
        return type(self)(op(self.to_dense()), dtype=dtype)

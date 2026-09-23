    def _difference(self, other, sort):

        if is_object_dtype(other):
            return self.astype(object).difference(other).astype(self.dtype)

        elif not is_dtype_equal(self.dtype, other.dtype):
            return self

        return self._setop(other, sort, opname="difference")

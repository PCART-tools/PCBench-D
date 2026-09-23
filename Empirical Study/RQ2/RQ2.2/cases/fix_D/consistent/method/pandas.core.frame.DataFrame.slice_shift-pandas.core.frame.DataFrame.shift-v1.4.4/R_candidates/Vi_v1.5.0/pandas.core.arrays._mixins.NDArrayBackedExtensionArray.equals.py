    def equals(self, other) -> bool:
        if type(self) is not type(other):
            return False
        if not is_dtype_equal(self.dtype, other.dtype):
            return False
        return bool(array_equivalent(self._ndarray, other._ndarray))

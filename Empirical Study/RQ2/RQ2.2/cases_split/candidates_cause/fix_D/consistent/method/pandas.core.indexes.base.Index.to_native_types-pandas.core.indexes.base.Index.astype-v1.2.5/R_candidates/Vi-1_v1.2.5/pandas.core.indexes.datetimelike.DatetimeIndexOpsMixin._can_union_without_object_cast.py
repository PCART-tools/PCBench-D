    def _can_union_without_object_cast(self, other) -> bool:
        return is_dtype_equal(self.dtype, other.dtype)

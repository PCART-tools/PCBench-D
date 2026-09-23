    def _should_compare(self, other) -> bool:
        if not super()._should_compare(other):
            return False
        other = unpack_nested_dtype(other)
        return other.closed == self.closed

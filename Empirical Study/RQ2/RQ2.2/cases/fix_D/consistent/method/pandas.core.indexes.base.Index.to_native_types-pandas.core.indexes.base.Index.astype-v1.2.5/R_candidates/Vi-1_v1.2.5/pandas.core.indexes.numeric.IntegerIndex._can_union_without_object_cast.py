    def _can_union_without_object_cast(self, other) -> bool:
        # See GH#26778, further casting may occur in NumericIndex._union
        return other.dtype == "f8" or other.dtype == self.dtype

    def equals(self, other) -> bool:
        """
        Determine if two Index objects contain the same elements.

        Returns
        -------
        bool
            True if "other" is an Index and it has the same elements as calling
            index; False otherwise.
        """
        if self.is_(other):
            return True

        if not isinstance(other, Index):
            return False

        if is_object_dtype(self) and not is_object_dtype(other):
            # if other is not object, use other's logic for coercion
            return other.equals(self)

        if isinstance(other, ABCMultiIndex):
            # d-level MultiIndex can equal d-tuple Index
            if not is_object_dtype(self.dtype):
                if self.nlevels != other.nlevels:
                    return False

        return array_equivalent(
            com.values_from_object(self), com.values_from_object(other)
        )

    def equals(self, other):
        """
        Determines if two Index objects contain the same elements.
        """
        if self.is_(other):
            return True

        if not isinstance(other, Index):
            return False

        if is_object_dtype(self) and not is_object_dtype(other):
            # if other is not object, use other's logic for coercion
            return other.equals(self)

        try:
            return array_equivalent(_values_from_object(self),
                                    _values_from_object(other))
        except:
            return False

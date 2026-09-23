    def equals(self, other):
        """
        Determines if two CategorialIndex objects contain the same elements.
        """
        if self.is_(other):
            return True

        try:
            other = self._is_dtype_compat(other)
            return array_equivalent(self._data, other)
        except (TypeError, ValueError):
            pass

        return False

    def equals(self, other):
        """
        Determines if two CategorialIndex objects contain the same elements.
        """
        if self.is_(other):
            return True

        if not isinstance(other, Index):
            return False

        try:
            other = self._is_dtype_compat(other)
            if isinstance(other, type(self)):
                other = other._data
            return self._data.equals(other)
        except (TypeError, ValueError):
            pass

        return False

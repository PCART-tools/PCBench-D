    def equals(self, other):
        """
        Determine if two CategoricalIndex objects contain the same elements.

        Returns
        -------
        bool
            If two CategoricalIndex objects have equal elements True,
            otherwise False.
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

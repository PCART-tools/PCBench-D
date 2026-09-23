    def equals(self, other):
        """
        Determines if two NDFrame objects contain the same elements. NaNs in
        the same location are considered equal.
        """
        if not isinstance(other, self._constructor):
            return False
        return self._data.equals(other._data)

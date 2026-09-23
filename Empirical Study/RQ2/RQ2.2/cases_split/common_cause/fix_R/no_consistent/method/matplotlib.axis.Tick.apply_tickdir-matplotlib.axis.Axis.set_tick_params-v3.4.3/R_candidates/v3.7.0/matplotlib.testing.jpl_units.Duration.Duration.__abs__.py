    def __abs__(self):
        """Return the absolute value of the duration."""
        return Duration(self._frame, abs(self._seconds))

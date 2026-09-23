    def __abs__(self):
        """Return the absolute value of this UnitDbl."""
        return UnitDbl(abs(self._value), self._units)

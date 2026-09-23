    def __neg__(self):
        """Return the negative value of this UnitDbl."""
        return UnitDbl(-self._value, self._units)

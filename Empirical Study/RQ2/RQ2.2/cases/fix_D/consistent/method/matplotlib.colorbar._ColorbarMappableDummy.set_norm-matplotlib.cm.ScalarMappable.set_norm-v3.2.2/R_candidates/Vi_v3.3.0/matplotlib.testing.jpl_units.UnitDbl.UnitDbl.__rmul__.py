    def __rmul__(self, lhs):
        """
        Scale a UnitDbl by a value.

        = INPUT VARIABLES
        - lhs     The scalar to multiply by.

        = RETURN VALUE
        - Returns the scaled UnitDbl.
        """
        return UnitDbl(self._value * lhs, self._units)

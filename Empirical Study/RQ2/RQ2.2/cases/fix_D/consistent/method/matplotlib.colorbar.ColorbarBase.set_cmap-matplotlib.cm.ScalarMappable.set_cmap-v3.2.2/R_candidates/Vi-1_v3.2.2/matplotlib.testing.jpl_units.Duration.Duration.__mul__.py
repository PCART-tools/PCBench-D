    def __mul__(self, rhs):
        """Scale a UnitDbl by a value.

        = INPUT VARIABLES
        - rhs     The scalar to multiply by.

        = RETURN VALUE
        - Returns the scaled Duration.
        """
        return Duration(self._frame, self._seconds * float(rhs))

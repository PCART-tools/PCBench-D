    def __rmul__(self, lhs):
        """
        Scale a Duration by a value.

        = INPUT VARIABLES
        - lhs     The scalar to multiply by.

        = RETURN VALUE
        - Returns the scaled Duration.
        """
        return Duration(self._frame, self._seconds * float(lhs))

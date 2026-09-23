    def __rdiv__(self, rhs):
        """Divide a Duration by a value.

        = INPUT VARIABLES
        - rhs     The scalar to divide by.

        = RETURN VALUE
        - Returns the scaled Duration.
        """
        return Duration(self._frame, rhs / self._seconds)

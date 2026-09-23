    def __sub__(self, rhs):
        """Subtract two Durations.

        = ERROR CONDITIONS
        - If the input rhs is not in the same frame, an error is thrown.

        = INPUT VARIABLES
        - rhs     The Duration to subtract.

        = RETURN VALUE
        - Returns the difference of ourselves and the input Duration.
        """
        self.checkSameFrame(rhs, "sub")
        return Duration(self._frame, self._seconds - rhs._seconds)

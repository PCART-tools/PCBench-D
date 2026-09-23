    def _cmp(self, rhs, op):
        """Compare two Durations.

        = INPUT VARIABLES
        - rhs     The Duration to compare against.
        - op      The function to do the comparison

        = RETURN VALUE
        - Returns op(self, rhs)
        """
        self.checkSameFrame(rhs, "compare")
        return op(self._seconds, rhs._seconds)

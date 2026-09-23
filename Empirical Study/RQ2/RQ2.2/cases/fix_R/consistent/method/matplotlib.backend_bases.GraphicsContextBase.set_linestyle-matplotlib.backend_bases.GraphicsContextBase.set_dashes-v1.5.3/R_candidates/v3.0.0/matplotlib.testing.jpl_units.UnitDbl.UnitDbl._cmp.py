    def _cmp(self, rhs, op):
        """Compare two UnitDbl's.

        = ERROR CONDITIONS
        - If the input rhs units are not the same as our units,
          an error is thrown.

        = INPUT VARIABLES
        - rhs     The UnitDbl to compare against.
        - op      The function to do the comparison

        = RETURN VALUE
        - Returns op(self, rhs)
        """
        self.checkSameUnits(rhs, "compare")
        return op(self._value, rhs._value)

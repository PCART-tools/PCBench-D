    def checkSameUnits(self, rhs, func):
        """Check to see if units are the same.

        = ERROR CONDITIONS
        - If the units of the rhs UnitDbl are not the same as our units,
          an error is thrown.

        = INPUT VARIABLES
        - rhs     The UnitDbl to check for the same units
        - func    The name of the function doing the check.
        """
        if self._units != rhs._units:
            msg = "Cannot %s units of different types.\n" \
                    "LHS: %s\n" \
                    "RHS: %s" % (func, self._units, rhs._units)
            raise ValueError(msg)

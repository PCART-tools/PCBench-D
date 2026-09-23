   def __div__( self, rhs ):
      """Divide a UnitDbl by a value.

      = INPUT VARIABLES
      - rhs    The scalar to divide by.

      = RETURN VALUE
      - Returns the scaled UnitDbl.
      """
      return UnitDbl( self._value / rhs, self._units )

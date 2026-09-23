   def __mul__( self, rhs ):
      """Scale a UnitDbl by a value.

      = INPUT VARIABLES
      - rhs    The scalar to multiply by.

      = RETURN VALUE
      - Returns the scaled UnitDbl.
      """
      return UnitDbl( self._value * rhs, self._units )

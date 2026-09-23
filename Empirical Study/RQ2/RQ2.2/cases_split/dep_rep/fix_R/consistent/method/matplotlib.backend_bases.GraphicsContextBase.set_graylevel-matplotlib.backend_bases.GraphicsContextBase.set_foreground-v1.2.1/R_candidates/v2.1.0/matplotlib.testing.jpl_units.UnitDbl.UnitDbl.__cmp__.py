   def __cmp__( self, rhs ):
      """Compare two UnitDbl's.

      = ERROR CONDITIONS
      - If the input rhs units are not the same as our units,
        an error is thrown.

      = INPUT VARIABLES
      - rhs    The UnitDbl to compare against.

      = RETURN VALUE
      - Returns -1 if self < rhs, 0 if self == rhs, +1 if self > rhs.
      """
      self.checkSameUnits( rhs, "compare" )
      return cmp( self._value, rhs._value )

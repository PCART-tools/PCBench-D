   def __add__( self, rhs ):
      """Add two UnitDbl's.

      = ERROR CONDITIONS
      - If the input rhs units are not the same as our units,
        an error is thrown.

      = INPUT VARIABLES
      - rhs    The UnitDbl to add.

      = RETURN VALUE
      - Returns the sum of ourselves and the input UnitDbl.
      """
      self.checkSameUnits( rhs, "add" )
      return UnitDbl( self._value + rhs._value, self._units )

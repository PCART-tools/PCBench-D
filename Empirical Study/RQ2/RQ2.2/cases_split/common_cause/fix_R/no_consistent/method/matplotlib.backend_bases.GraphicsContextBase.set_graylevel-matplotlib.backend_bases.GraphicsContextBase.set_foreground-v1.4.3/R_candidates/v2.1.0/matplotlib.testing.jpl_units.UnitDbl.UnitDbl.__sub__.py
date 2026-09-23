   def __sub__( self, rhs ):
      """Subtract two UnitDbl's.

      = ERROR CONDITIONS
      - If the input rhs units are not the same as our units,
        an error is thrown.

      = INPUT VARIABLES
      - rhs    The UnitDbl to subtract.

      = RETURN VALUE
      - Returns the difference of ourselves and the input UnitDbl.
      """
      self.checkSameUnits( rhs, "subtract" )
      return UnitDbl( self._value - rhs._value, self._units )

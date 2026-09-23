   def __cmp__( self, rhs ):
      """Compare two Durations.

      = ERROR CONDITIONS
      - If the input rhs is not in the same frame, an error is thrown.

      = INPUT VARIABLES
      - rhs    The Duration to compare against.

      = RETURN VALUE
      - Returns -1 if self < rhs, 0 if self == rhs, +1 if self > rhs.
      """
      self.checkSameFrame( rhs, "compare" )
      return cmp( self._seconds, rhs._seconds )

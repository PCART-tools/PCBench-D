   def __nonzero__( self ):
      """Compare two Durations.

      = INPUT VARIABLES
      - rhs    The Duration to compare against.

      = RETURN VALUE
      - Returns -1 if self < rhs, 0 if self == rhs, +1 if self > rhs.
      """
      return self._seconds != 0

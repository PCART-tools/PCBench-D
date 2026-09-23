   def __cmp__( self, rhs ):
      """Compare two Epoch's.

      = INPUT VARIABLES
      - rhs    The Epoch to compare against.

      = RETURN VALUE
      - Returns -1 if self < rhs, 0 if self == rhs, +1 if self > rhs.
      """
      t = self
      if self._frame != rhs._frame:
         t = self.convert( rhs._frame )

      if t._jd != rhs._jd:
         return cmp( t._jd, rhs._jd )

      return cmp( t._seconds, rhs._seconds )

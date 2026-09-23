   def __add__( self, rhs ):
      """Add a duration to an Epoch.

      = INPUT VARIABLES
      - rhs    The Epoch to subtract.

      = RETURN VALUE
      - Returns the difference of ourselves and the input Epoch.
      """
      t = self
      if self._frame != rhs.frame():
         t = self.convert( rhs._frame )

      sec = t._seconds + rhs.seconds()

      return Epoch( t._frame, sec, t._jd )

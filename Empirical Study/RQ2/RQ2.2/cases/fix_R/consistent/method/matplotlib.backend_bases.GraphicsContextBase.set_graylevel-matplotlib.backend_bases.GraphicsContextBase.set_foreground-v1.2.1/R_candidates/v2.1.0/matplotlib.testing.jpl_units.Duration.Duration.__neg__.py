   def __neg__( self ):
      """Return the negative value of this Duration."""
      return Duration( self._frame, -self._seconds )

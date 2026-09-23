   def __str__( self ):
      """Print the Epoch."""
      return "%22.15e %s" % ( self.julianDate( self._frame ), self._frame )

   def __init__( self, frame, seconds ):
      """Create a new Duration object.

      = ERROR CONDITIONS
      - If the input frame is not in the allowed list, an error is thrown.

      = INPUT VARIABLES
      - frame    The frame of the duration.  Must be 'ET' or 'UTC'
      - seconds  The number of seconds in the Duration.
      """
      if frame not in self.allowed:
         msg = "Input frame '%s' is not one of the supported frames of %s" \
               % ( frame, str( self.allowed ) )
         raise ValueError( msg )

      self._frame = frame
      self._seconds = seconds

   def checkSameFrame( self, rhs, func ):
      """Check to see if frames are the same.

      = ERROR CONDITIONS
      - If the frame of the rhs Duration is not the same as our frame,
        an error is thrown.

      = INPUT VARIABLES
      - rhs    The Duration to check for the same frame
      - func   The name of the function doing the check.
      """
      if self._frame != rhs._frame:
         msg = "Cannot %s Duration's with different frames.\n" \
               "LHS: %s\n" \
               "RHS: %s" % ( func, self._frame, rhs._frame )
         raise ValueError( msg )

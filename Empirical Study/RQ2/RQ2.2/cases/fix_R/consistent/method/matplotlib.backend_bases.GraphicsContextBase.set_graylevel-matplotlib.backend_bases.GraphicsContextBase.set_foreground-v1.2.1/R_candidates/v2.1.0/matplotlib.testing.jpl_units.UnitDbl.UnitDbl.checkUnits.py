   def checkUnits( self, units ):
      """Check to see if some units are valid.

      = ERROR CONDITIONS
      - If the input units are not in the allowed list, an error is thrown.

      = INPUT VARIABLES
      - units    The string name of the units to check.
      """
      if units not in self.allowed:
         msg = "Input units '%s' are not one of the supported types of %s" \
               % ( units, str( list(six.iterkeys(self.allowed)) ) )
         raise ValueError( msg )

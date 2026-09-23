   def __nonzero__( self ):
      """Test a UnitDbl for a non-zero value.

      = RETURN VALUE
      - Returns true if the value is non-zero.
      """
      if six.PY3:
          return self._value.__bool__()
      else:
          return self._value.__nonzero__()

   @staticmethod
   def default_units( value, axis ):
      """: Return the default unit for value, or None.

      = INPUT VARIABLES
      - axis    The axis using this converter.
      - value   The value or list of values that need units.

      = RETURN VALUE
      - Returns the default units to use for value.
      Return the default unit for value, or None.
      """

      # The default behavior for string indexing.
      return "indexed"

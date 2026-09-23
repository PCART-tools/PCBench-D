   @staticmethod
   def duration2float( value ):
      """: Convert a Duration value to a float suitible for plotting as a
           python datetime object.

      = INPUT VARIABLES
      - value   A Duration or list of Durations that need to be converted.

      = RETURN VALUE
      - Returns the value parameter converted to floats.
      """
      return value.days()

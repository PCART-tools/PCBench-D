   @staticmethod
   def axisinfo( unit, axis ):
      """: Returns information on how to handle an axis that has Epoch data.

      = INPUT VARIABLES
      - unit    The units to use for a axis with Epoch data.

      = RETURN VALUE
      - Returns a matplotlib AxisInfo data structure that contains
        minor/major formatters, major/minor locators, and default
        label information.
      """

      majloc = date_ticker.AutoDateLocator()
      majfmt = date_ticker.AutoDateFormatter( majloc )

      return units.AxisInfo( majloc = majloc,
                             majfmt = majfmt,
                             label = unit )

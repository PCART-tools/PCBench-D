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
      # Delay-load due to circular dependencies.
      import matplotlib.testing.jpl_units as U

      # Check to see if the value used for units is a string unit value
      # or an actual instance of a UnitDbl so that we can use the unit
      # value for the default axis label value.
      if ( unit ):
         if ( isinstance( unit, six.string_types ) ):
            label = unit
         else:
            label = unit.label()
      else:
         label = None

      if ( label == "deg" ) and isinstance( axis.axes, polar.PolarAxes ):
         # If we want degrees for a polar plot, use the PolarPlotFormatter
         majfmt = polar.PolarAxes.ThetaFormatter()
      else:
         majfmt = U.UnitDblFormatter( useOffset = False )

      return units.AxisInfo( majfmt = majfmt, label = label )

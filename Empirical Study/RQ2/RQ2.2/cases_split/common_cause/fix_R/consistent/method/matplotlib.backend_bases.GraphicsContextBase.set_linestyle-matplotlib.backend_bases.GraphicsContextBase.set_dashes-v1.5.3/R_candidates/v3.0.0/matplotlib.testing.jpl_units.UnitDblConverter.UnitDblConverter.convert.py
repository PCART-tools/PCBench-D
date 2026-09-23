    @staticmethod
    def convert(value, unit, axis):
        """: Convert value using unit to a float.  If value is a sequence, return
        the converted sequence.

        = INPUT VARIABLES
        - value    The value or list of values that need to be converted.
        - unit     The units to use for a axis with Epoch data.

        = RETURN VALUE
        - Returns the value parameter converted to floats.
        """
        # Delay-load due to circular dependencies.
        import matplotlib.testing.jpl_units as U

        isNotUnitDbl = True

        if iterable(value) and not isinstance(value, str):
            if len(value) == 0:
                return []
            else:
                return [UnitDblConverter.convert(x, unit, axis) for x in value]

        # We need to check to see if the incoming value is actually a
        # UnitDbl and set a flag.  If we get an empty list, then just
        # return an empty list.
        if (isinstance(value, U.UnitDbl)):
            isNotUnitDbl = False

        # If the incoming value behaves like a number, but is not a UnitDbl,
        # then just return it because we don't know how to convert it
        # (or it is already converted)
        if (isNotUnitDbl and units.ConversionInterface.is_numlike(value)):
            return value

        # If no units were specified, then get the default units to use.
        if unit is None:
            unit = UnitDblConverter.default_units(value, axis)

        # Convert the incoming UnitDbl value/values to float/floats
        if isinstance(axis.axes, polar.PolarAxes) and value.type() == "angle":
            # Guarantee that units are radians for polar plots.
            return value.convert("rad")

        return value.convert(unit)

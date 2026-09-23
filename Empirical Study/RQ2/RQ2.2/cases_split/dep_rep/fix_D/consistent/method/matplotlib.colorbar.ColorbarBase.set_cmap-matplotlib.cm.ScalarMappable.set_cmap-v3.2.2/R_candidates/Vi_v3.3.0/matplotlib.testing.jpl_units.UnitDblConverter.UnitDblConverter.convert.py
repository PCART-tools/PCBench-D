    @staticmethod
    def convert(value, unit, axis):
        # docstring inherited
        if not cbook.is_scalar_or_string(value):
            return [UnitDblConverter.convert(x, unit, axis) for x in value]
        # If the incoming value behaves like a number,
        # then just return it because we don't know how to convert it
        # (or it is already converted)
        if units.ConversionInterface.is_numlike(value):
            return value
        # If no units were specified, then get the default units to use.
        if unit is None:
            unit = UnitDblConverter.default_units(value, axis)
        # Convert the incoming UnitDbl value/values to float/floats
        if isinstance(axis.axes, polar.PolarAxes) and value.type() == "angle":
            # Guarantee that units are radians for polar plots.
            return value.convert("rad")
        return value.convert(unit)

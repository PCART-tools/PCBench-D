    @staticmethod
    def default_units(value, axis):
        # docstring inherited
        # Determine the default units based on the user preferences set for
        # default units when printing a UnitDbl.
        if cbook.is_scalar_or_string(value):
            return UnitDblConverter.defaults[value.type()]
        else:
            return UnitDblConverter.default_units(value[0], axis)

    @staticmethod
    def default_units(value, axis):
        """: Return the default unit for value, or None.

        = INPUT VARIABLES
        - value    The value or list of values that need units.

        = RETURN VALUE
        - Returns the default units to use for value.
        Return the default unit for value, or None.
        """
        # Determine the default units based on the user preferences set for
        # default units when printing a UnitDbl.
        if cbook.is_scalar_or_string(value):
            return UnitDblConverter.defaults[value.type()]
        else:
            return UnitDblConverter.default_units(value[0], axis)

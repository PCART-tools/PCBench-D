    @staticmethod
    def default_units(value, axis):
        """: Return the default unit for value, or None.

        = INPUT VARIABLES
        - value    The value or list of values that need units.

        = RETURN VALUE
        - Returns the default units to use for value.
        """
        if cbook.is_scalar_or_string(value):
            return value.frame()
        else:
            return EpochConverter.default_units(value[0], axis)

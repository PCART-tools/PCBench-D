    @staticmethod
    def default_units(value, axis):
        """: Return the default unit for value, or None.

        = INPUT VARIABLES
        - value    The value or list of values that need units.

        = RETURN VALUE
        - Returns the default units to use for value.
        """
        frame = None
        if iterable(value) and not isinstance(value, str):
            return EpochConverter.default_units(value[0], axis)
        else:
            frame = value.frame()

        return frame

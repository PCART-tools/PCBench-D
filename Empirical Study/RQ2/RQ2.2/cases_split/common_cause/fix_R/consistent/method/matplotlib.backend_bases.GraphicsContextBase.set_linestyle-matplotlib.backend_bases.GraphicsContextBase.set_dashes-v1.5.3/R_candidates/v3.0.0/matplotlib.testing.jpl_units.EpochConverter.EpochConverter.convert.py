    @staticmethod
    def convert(value, unit, axis):
        """: Convert value using unit to a float.  If value is a sequence, return
        the converted sequence.

        = INPUT VARIABLES
        - value    The value or list of values that need to be converted.
        - unit     The units to use for an axis with Epoch data.

        = RETURN VALUE
        - Returns the value parameter converted to floats.
        """
        # Delay-load due to circular dependencies.
        import matplotlib.testing.jpl_units as U

        isNotEpoch = True
        isDuration = False

        if iterable(value) and not isinstance(value, str):
            if len(value) == 0:
                return []
            else:
                return [EpochConverter.convert(x, unit, axis) for x in value]

        if isinstance(value, U.Epoch):
            isNotEpoch = False
        elif isinstance(value, U.Duration):
            isDuration = True

        if (isNotEpoch and not isDuration and
           units.ConversionInterface.is_numlike(value)):
            return value

        if unit is None:
            unit = EpochConverter.default_units(value, axis)

        if isDuration:
            return EpochConverter.duration2float(value)
        else:
            return EpochConverter.epoch2float(value, unit)

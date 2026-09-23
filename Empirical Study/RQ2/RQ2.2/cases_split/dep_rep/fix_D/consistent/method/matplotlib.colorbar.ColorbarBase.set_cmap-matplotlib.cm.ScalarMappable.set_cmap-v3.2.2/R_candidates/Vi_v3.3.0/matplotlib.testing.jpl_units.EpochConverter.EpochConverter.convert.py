    @staticmethod
    def convert(value, unit, axis):
        # docstring inherited

        # Delay-load due to circular dependencies.
        import matplotlib.testing.jpl_units as U

        if not cbook.is_scalar_or_string(value):
            return [EpochConverter.convert(x, unit, axis) for x in value]
        if units.ConversionInterface.is_numlike(value):
            return value
        if unit is None:
            unit = EpochConverter.default_units(value, axis)
        if isinstance(value, U.Duration):
            return EpochConverter.duration2float(value)
        else:
            return EpochConverter.epoch2float(value, unit)

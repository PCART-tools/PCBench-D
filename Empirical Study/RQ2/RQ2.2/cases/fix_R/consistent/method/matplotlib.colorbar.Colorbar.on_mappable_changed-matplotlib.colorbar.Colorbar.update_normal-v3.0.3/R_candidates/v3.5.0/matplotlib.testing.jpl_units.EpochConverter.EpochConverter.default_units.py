    @staticmethod
    def default_units(value, axis):
        # docstring inherited
        if cbook.is_scalar_or_string(value):
            return value.frame()
        else:
            return EpochConverter.default_units(value[0], axis)

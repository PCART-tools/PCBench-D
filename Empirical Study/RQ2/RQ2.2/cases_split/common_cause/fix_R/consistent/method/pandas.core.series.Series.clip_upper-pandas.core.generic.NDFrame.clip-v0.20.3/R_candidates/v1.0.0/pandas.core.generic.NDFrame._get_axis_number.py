    @classmethod
    def _get_axis_number(cls, axis):
        axis = cls._AXIS_ALIASES.get(axis, axis)
        if is_integer(axis):
            if axis in cls._AXIS_NAMES:
                return axis
        else:
            try:
                return cls._AXIS_NUMBERS[axis]
            except KeyError:
                pass
        raise ValueError(f"No axis named {axis} for object type {cls}")

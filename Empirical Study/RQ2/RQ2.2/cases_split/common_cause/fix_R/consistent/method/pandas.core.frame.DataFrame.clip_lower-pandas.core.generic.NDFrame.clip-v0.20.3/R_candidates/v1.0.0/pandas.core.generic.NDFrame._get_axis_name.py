    @classmethod
    def _get_axis_name(cls, axis):
        axis = cls._AXIS_ALIASES.get(axis, axis)
        if isinstance(axis, str):
            if axis in cls._AXIS_NUMBERS:
                return axis
        else:
            try:
                return cls._AXIS_NAMES[axis]
            except KeyError:
                pass
        raise ValueError(f"No axis named {axis} for object type {cls}")

    @final
    @classmethod
    def _get_axis_number(cls, axis: Axis) -> int:
        try:
            return cls._AXIS_TO_AXIS_NUMBER[axis]
        except KeyError:
            raise ValueError(f"No axis named {axis} for object type {cls.__name__}")

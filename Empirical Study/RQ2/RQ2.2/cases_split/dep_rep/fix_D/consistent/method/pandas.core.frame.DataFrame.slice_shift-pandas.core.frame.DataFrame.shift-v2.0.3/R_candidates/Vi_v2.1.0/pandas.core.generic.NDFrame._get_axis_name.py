    @final
    @classmethod
    def _get_axis_name(cls, axis: Axis) -> Literal["index", "columns"]:
        axis_number = cls._get_axis_number(axis)
        return cls._AXIS_ORDERS[axis_number]

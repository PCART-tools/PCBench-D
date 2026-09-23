    @final
    @classmethod
    def _get_block_manager_axis(cls, axis: Axis) -> int:
        """Map the axis to the block_manager axis."""
        axis = cls._get_axis_number(axis)
        ndim = cls._AXIS_LEN
        if ndim == 2:
            # i.e. DataFrame
            return 1 - axis
        return axis

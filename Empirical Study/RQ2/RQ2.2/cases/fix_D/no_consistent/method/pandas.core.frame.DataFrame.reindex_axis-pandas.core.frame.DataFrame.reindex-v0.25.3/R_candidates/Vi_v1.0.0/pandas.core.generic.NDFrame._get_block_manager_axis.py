    @classmethod
    def _get_block_manager_axis(cls, axis):
        """Map the axis to the block_manager axis."""
        axis = cls._get_axis_number(axis)
        if cls._AXIS_REVERSED:
            m = cls._AXIS_LEN - 1
            return m - axis
        return axis

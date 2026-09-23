    def _get_block_manager_axis(self, axis):
        """Map the axis to the block_manager axis."""
        axis = self._get_axis_number(axis)
        if self._AXIS_REVERSED:
            m = self._AXIS_LEN - 1
            return m - axis
        return axis

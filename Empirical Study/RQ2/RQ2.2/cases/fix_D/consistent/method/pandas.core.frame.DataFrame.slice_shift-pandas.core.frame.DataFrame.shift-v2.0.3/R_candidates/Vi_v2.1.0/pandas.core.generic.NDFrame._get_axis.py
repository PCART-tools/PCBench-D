    @final
    def _get_axis(self, axis: Axis) -> Index:
        axis_number = self._get_axis_number(axis)
        assert axis_number in {0, 1}
        return self.index if axis_number == 0 else self.columns

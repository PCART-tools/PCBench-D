    def _flex_cmp_method(self, other, op, *, axis: Axis = "columns", level=None):
        axis = self._get_axis_number(axis) if axis is not None else 1

        self, other = self._align_for_op(other, axis, flex=True, level=level)

        new_data = self._dispatch_frame_op(other, op, axis=axis)
        return self._construct_result(new_data)

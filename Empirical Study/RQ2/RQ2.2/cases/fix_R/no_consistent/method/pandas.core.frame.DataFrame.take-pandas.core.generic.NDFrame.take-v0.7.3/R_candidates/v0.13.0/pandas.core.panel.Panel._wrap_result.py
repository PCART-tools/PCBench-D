    def _wrap_result(self, result, axis):
        axis = self._get_axis_name(axis)
        axes = self._get_plane_axes(axis)
        if result.ndim == 2 and axis != self._info_axis_name:
            result = result.T

        return self._construct_return_type(result, axes)

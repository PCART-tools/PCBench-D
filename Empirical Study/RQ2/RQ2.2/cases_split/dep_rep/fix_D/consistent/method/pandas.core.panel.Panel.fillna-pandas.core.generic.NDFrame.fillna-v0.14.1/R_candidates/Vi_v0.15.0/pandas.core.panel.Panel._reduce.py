    def _reduce(self, op, axis=0, skipna=True, numeric_only=None,
                filter_type=None, name=None, **kwds):
        axis_name = self._get_axis_name(axis)
        axis_number = self._get_axis_number(axis_name)
        f = lambda x: op(x, axis=axis_number, skipna=skipna, **kwds)

        result = f(self.values)

        axes = self._get_plane_axes(axis_name)
        if result.ndim == 2 and axis_name != self._info_axis_name:
            result = result.T

        return self._construct_return_type(result, axes)

    def _combine_frame(self, other, func, axis=0):
        index, columns = self._get_plane_axes(axis)
        axis = self._get_axis_number(axis)

        other = other.reindex(index=index, columns=columns)

        with np.errstate(all='ignore'):
            if axis == 0:
                new_values = func(self.values, other.values)
            elif axis == 1:
                new_values = func(self.values.swapaxes(0, 1), other.values.T)
                new_values = new_values.swapaxes(0, 1)
            elif axis == 2:
                new_values = func(self.values.swapaxes(0, 2), other.values)
                new_values = new_values.swapaxes(0, 2)

        return self._constructor(new_values, self.items, self.major_axis,
                                 self.minor_axis)

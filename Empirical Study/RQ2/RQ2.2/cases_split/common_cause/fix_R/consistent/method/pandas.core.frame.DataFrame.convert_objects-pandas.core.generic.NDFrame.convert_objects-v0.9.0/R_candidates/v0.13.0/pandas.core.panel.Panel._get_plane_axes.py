    def _get_plane_axes(self, axis):
        """
        Get my plane axes: these are already
        (as compared with higher level planes),
        as we are returning a DataFrame axes
        """
        axis = self._get_axis_name(axis)

        if axis == 'major_axis':
            index = self.minor_axis
            columns = self.items
        if axis == 'minor_axis':
            index = self.major_axis
            columns = self.items
        elif axis == 'items':
            index = self.major_axis
            columns = self.minor_axis

        return index, columns

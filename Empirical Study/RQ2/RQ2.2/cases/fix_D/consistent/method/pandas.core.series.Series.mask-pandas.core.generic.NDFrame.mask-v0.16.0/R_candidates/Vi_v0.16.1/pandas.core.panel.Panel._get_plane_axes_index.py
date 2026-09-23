    def _get_plane_axes_index(self, axis):
        """
        Get my plane axes indexes: these are already
        (as compared with higher level planes),
        as we are returning a DataFrame axes indexes
        """
        axis_name = self._get_axis_name(axis)

        if axis_name == 'major_axis':
            index = 'minor_axis'
            columns = 'items'
        if axis_name == 'minor_axis':
            index = 'major_axis'
            columns = 'items'
        elif axis_name == 'items':
            index = 'major_axis'
            columns = 'minor_axis'

        return index, columns

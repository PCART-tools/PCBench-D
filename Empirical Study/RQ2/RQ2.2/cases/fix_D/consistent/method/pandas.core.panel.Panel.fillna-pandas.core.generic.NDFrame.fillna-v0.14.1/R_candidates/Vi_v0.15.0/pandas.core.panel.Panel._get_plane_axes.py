    def _get_plane_axes(self, axis):
        """
        Get my plane axes indexes: these are already
        (as compared with higher level planes),
        as we are returning a DataFrame axes
        """
        return [ self._get_axis(axi) for axi in self._get_plane_axes_index(axis) ]

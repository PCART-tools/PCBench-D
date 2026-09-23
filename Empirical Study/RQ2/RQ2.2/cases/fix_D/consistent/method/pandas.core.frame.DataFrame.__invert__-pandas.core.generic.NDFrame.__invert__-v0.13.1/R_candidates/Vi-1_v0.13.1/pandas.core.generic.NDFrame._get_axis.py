    def _get_axis(self, axis):
        name = self._get_axis_name(axis)
        return getattr(self, name)

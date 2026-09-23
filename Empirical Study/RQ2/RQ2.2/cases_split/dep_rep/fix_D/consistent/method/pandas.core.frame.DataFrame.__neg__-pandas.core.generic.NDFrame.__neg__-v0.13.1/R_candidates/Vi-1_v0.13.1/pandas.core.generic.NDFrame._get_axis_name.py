    def _get_axis_name(self, axis):
        axis = self._AXIS_ALIASES.get(axis, axis)
        if isinstance(axis, string_types):
            if axis in self._AXIS_NUMBERS:
                return axis
        else:
            try:
                return self._AXIS_NAMES[axis]
            except:
                pass
        raise ValueError('No axis named {0} for object type {1}'
                         .format(axis, type(self)))

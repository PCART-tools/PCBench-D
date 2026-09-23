    def _set_axis(self, axis, value, check_axis=True):
        cur_axis = self.axes[axis]
        value = _ensure_index(value)

        if check_axis and len(value) != len(cur_axis):
            raise ValueError('Length mismatch: Expected axis has %d elements, '
                             'new values have %d elements' % (len(cur_axis),
                                                              len(value)))

        self.axes[axis] = value
        self._shape = None
        return cur_axis, value

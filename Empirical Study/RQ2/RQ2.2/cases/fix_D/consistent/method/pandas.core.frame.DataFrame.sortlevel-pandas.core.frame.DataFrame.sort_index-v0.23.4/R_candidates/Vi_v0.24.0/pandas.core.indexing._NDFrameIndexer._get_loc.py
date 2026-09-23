    def _get_loc(self, key, axis=None):
        if axis is None:
            axis = self.axis
        return self.obj._ixs(key, axis=axis)

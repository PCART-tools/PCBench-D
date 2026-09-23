    def _slice(self, obj, axis=None, kind=None):
        if axis is None:
            axis = self.axis
        return self.obj._slice(obj, axis=axis, kind=kind)

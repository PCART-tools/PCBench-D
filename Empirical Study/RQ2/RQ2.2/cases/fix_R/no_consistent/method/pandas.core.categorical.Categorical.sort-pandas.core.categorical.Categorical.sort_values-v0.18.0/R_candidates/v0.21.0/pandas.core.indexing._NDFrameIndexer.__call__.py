    def __call__(self, axis=None):
        # we need to return a copy of ourselves
        new_self = self.__class__(self.obj, self.name)

        if axis is not None:
            axis = self.obj._get_axis_number(axis)
        new_self.axis = axis
        return new_self

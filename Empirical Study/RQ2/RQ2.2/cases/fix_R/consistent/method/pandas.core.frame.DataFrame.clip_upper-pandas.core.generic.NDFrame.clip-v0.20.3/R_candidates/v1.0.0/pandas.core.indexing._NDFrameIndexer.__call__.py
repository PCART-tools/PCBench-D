    def __call__(self, axis=None):
        # we need to return a copy of ourselves
        new_self = type(self)(self.name, self.obj)

        if axis is not None:
            axis = self.obj._get_axis_number(axis)
        new_self.axis = axis
        return new_self

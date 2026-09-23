    def __array_wrap__(self, result, copy=False):
        d = self._construct_axes_dict(self._AXIS_ORDERS, copy=copy)
        return self._constructor(result, **d).__finalize__(self)

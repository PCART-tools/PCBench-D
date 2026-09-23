    def __array_wrap__(self, result, context=None):
        d = self._construct_axes_dict(self._AXIS_ORDERS, copy=False)
        return self._constructor(result, **d).__finalize__(self)

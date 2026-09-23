
    def __neg__(self):
        arr = operator.neg(self.values)
        return self._wrap_array(arr, self.axes, copy=False)

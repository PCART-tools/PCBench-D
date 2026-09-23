
    def __invert__(self):
        arr = operator.inv(self.values)
        return self._wrap_array(arr, self.axes, copy=False)

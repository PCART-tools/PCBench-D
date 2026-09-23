    def __invert__(self):
        arr = operator.inv(_values_from_object(self))
        return self._wrap_array(arr, self.axes, copy=False)

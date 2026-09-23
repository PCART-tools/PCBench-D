    def __neg__(self):
        arr = operator.neg(_values_from_object(self))
        return self._wrap_array(arr, self.axes, copy=False)

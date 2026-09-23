    def __invert__(self):
        arr = operator.inv(self.values)
        return self._constructor(arr, self.index).__finalize__(self)

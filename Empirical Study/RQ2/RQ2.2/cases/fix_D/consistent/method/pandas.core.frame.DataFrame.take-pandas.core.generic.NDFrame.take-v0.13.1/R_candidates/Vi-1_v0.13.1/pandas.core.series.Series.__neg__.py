    def __neg__(self):
        arr = operator.neg(self.values)
        return self._constructor(arr, self.index).__finalize__(self)

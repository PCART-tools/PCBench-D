    def __getitem__(self, item):
        if isinstance(item, type(self)):
            item = item._ndarray

        result = self._ndarray[item]
        if not lib.is_scalar(item):
            result = type(self)(result)
        return result

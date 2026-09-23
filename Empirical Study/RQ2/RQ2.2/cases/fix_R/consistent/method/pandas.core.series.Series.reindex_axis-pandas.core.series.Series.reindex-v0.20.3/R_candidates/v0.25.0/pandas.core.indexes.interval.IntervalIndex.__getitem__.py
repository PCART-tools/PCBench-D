    def __getitem__(self, value):
        result = self._data[value]
        if isinstance(result, IntervalArray):
            return self._shallow_copy(result)
        else:
            # scalar
            return result

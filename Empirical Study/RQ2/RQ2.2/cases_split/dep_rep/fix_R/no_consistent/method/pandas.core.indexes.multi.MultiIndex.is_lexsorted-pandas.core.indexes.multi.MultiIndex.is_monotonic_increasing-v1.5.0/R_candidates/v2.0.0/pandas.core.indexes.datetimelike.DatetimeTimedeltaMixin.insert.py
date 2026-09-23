    @doc(NDArrayBackedExtensionIndex.insert)
    def insert(self, loc: int, item):
        result = super().insert(loc, item)
        if isinstance(result, type(self)):
            # i.e. parent class method did not cast
            result._data._freq = self._get_insert_freq(loc, item)
        return result

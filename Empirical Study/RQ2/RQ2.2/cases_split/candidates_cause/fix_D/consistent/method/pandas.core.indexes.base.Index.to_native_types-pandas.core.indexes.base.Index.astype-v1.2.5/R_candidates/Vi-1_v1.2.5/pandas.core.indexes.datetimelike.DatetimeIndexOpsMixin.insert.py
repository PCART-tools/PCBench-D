    @doc(NDArrayBackedExtensionIndex.insert)
    def insert(self, loc: int, item):
        result = super().insert(loc, item)

        result._data._freq = self._get_insert_freq(loc, item)
        return result

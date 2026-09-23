    @doc(NDArrayBackedExtensionIndex.delete)
    def delete(self, loc):
        result = super().delete(loc)
        result._data._freq = self._get_delete_freq(loc)
        return result

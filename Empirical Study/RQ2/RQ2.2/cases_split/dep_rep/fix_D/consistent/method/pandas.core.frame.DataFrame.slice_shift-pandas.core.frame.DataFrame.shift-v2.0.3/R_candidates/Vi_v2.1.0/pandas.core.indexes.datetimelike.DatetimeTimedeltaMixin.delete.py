    @doc(NDArrayBackedExtensionIndex.delete)
    def delete(self, loc) -> Self:
        result = super().delete(loc)
        result._data._freq = self._get_delete_freq(loc)
        return result

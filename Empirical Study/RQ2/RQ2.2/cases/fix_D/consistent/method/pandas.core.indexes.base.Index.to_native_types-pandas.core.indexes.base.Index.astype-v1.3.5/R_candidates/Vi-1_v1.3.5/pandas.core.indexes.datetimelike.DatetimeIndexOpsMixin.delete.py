    @doc(NDArrayBackedExtensionIndex.delete)
    def delete(self: _T, loc) -> _T:
        result = super().delete(loc)
        result._data._freq = self._get_delete_freq(loc)
        return result

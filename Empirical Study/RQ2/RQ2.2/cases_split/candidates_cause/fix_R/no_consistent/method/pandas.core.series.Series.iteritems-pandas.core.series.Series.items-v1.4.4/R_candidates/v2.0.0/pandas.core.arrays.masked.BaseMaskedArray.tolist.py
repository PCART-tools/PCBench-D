    @doc(ExtensionArray.tolist)
    def tolist(self):
        if self.ndim > 1:
            return [x.tolist() for x in self]
        dtype = None if self._hasna else self._data.dtype
        return self.to_numpy(dtype=dtype).tolist()

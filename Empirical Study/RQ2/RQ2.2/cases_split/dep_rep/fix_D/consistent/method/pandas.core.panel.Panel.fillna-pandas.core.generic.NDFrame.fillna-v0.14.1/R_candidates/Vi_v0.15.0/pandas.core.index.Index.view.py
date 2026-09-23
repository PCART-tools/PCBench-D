    def view(self, cls=None):
        if cls is not None and not issubclass(cls, Index):
            result = self._data.view(cls)
        else:
            result = self._shallow_copy()
        if isinstance(result, Index):
            result._id = self._id
        return result

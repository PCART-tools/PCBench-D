    def __getitem__(self, key):
        result = self._data.array._str_getitem(key)
        return self._wrap_result(result)

    @copy(str_get)
    def get(self, i):
        result = str_get(self._data, i)
        return self._wrap_result(result)

    @copy(str_get)
    def get(self, i):
        result = str_get(self._parent, i)
        return self._wrap_result(result)

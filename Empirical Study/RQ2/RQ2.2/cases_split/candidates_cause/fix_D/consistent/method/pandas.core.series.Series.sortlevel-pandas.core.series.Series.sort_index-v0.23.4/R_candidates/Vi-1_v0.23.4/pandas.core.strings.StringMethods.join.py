    @copy(str_join)
    def join(self, sep):
        result = str_join(self._data, sep)
        return self._wrap_result(result)

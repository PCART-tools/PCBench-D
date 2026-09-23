    @copy(str_repeat)
    def repeat(self, repeats):
        result = str_repeat(self._data, repeats)
        return self._wrap_result(result)

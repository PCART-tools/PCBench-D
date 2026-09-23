    @copy(str_wrap)
    def wrap(self, width, **kwargs):
        result = str_wrap(self._data, width, **kwargs)
        return self._wrap_result(result)

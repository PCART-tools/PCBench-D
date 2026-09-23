    @copy(str_wrap)
    def wrap(self, width, **kwargs):
        result = str_wrap(self._parent, width, **kwargs)
        return self._wrap_result(result)

    @copy(str_wrap)
    @forbid_nonstring_types(["bytes"])
    def wrap(self, width, **kwargs):
        result = str_wrap(self._parent, width, **kwargs)
        return self._wrap_result(result)

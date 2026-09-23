    @copy(str_join)
    @forbid_nonstring_types(["bytes"])
    def join(self, sep):
        result = str_join(self._parent, sep)
        return self._wrap_result(result)

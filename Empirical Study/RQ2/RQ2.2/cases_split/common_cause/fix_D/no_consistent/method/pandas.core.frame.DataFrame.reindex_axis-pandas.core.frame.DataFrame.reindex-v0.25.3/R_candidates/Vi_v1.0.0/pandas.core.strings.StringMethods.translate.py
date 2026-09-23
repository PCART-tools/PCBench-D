    @copy(str_translate)
    @forbid_nonstring_types(["bytes"])
    def translate(self, table):
        result = str_translate(self._parent, table)
        return self._wrap_result(result)

    @copy(str_slice_replace)
    @forbid_nonstring_types(["bytes"])
    def slice_replace(self, start=None, stop=None, repl=None):
        result = str_slice_replace(self._parent, start, stop, repl)
        return self._wrap_result(result)

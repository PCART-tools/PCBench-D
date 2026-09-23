    @copy(str_encode)
    @forbid_nonstring_types(["bytes"])
    def encode(self, encoding, errors="strict"):
        result = str_encode(self._parent, encoding, errors)
        return self._wrap_result(result, returns_string=False)

    @copy(str_encode)
    def encode(self, encoding, errors="strict"):
        result = str_encode(self._parent, encoding, errors)
        return self._wrap_result(result)

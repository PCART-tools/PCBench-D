    @copy(str_decode)
    def decode(self, encoding, errors="strict"):
        result = str_decode(self._data, encoding, errors)
        return self._wrap_result(result)

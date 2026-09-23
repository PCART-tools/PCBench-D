    @copy(str_decode)
    def decode(self, encoding, errors="strict"):
        # need to allow bytes here
        result = str_decode(self._parent, encoding, errors)
        # TODO: Not sure how to handle this.
        return self._wrap_result(result, returns_string=False)

    def _str_encode(self, encoding: str, errors: str = "strict"):
        predicate = lambda val: val.encode(encoding, errors)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))

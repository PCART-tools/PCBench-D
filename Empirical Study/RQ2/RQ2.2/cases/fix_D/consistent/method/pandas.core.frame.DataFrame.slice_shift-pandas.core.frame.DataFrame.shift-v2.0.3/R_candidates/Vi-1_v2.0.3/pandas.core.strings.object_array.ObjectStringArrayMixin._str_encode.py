    def _str_encode(self, encoding, errors: str = "strict"):
        f = lambda x: x.encode(encoding, errors=errors)
        return self._str_map(f, dtype=object)

    def _str_index(self, sub: str, start: int = 0, end: int | None = None):
        predicate = lambda val: val.index(sub, start, end)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))

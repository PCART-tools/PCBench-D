    def _str_rindex(self, sub: str, start: int = 0, end: int | None = None):
        predicate = lambda val: val.rindex(sub, start, end)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))

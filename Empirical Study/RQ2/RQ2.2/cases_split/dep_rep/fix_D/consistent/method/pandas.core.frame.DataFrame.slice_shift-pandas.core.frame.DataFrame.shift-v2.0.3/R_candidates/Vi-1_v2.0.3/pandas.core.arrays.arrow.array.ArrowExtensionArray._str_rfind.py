    def _str_rfind(self, sub: str, start: int = 0, end=None):
        predicate = lambda val: val.rfind(sub, start, end)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))

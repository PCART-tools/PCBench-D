    def _str_rpartition(self, sep: str, expand: bool):
        predicate = lambda val: val.rpartition(sep)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))

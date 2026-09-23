    def _str_join(self, sep: str):
        if pa.types.is_string(self._pa_array.type):
            result = self._apply_elementwise(list)
            result = pa.chunked_array(result, type=pa.list_(pa.string()))
        else:
            result = self._pa_array
        return type(self)(pc.binary_join(result, sep))

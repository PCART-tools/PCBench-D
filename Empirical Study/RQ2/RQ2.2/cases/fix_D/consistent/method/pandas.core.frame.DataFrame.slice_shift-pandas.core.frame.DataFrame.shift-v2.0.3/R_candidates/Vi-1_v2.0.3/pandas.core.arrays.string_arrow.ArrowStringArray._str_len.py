    def _str_len(self):
        result = pc.utf8_length(self._data)
        return Int64Dtype().__from_arrow__(result)

    def _str_len(self):
        result = pc.utf8_length(self._pa_array)
        return Int64Dtype().__from_arrow__(result)

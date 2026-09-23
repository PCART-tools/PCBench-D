    def _str_len(self):
        if pa_version_under4p0:
            return super()._str_len()

        result = pc.utf8_length(self._data)
        return Int64Dtype().__from_arrow__(result)
